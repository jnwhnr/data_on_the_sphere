import bpy
import os
import glob
import math
import sys

# ==============================================================================
# CONFIGURATION SECTION - MODIFY THESE VALUES
# ==============================================================================

# A) GeoTIFF Map Selection
GEOTIFF_PATH = None  # Set to None to auto-find in Input folder, or specify full path

# B) Color Selection - Choose from individual or common libraries
DISPLAY_COLOR = "temperature"     # SCIENTIFIC BEST PRACTICES:
                              # For most data: "viridis", "plasma", "cividis" (perceptually uniform)
                              # For temperature anomalies: "coolwarm", "RdBu_r" (diverging)  
                              # For precipitation: "Blues", "BuGn", "jw_precip"
                              # For elevation: "terrain", "gist_earth", "earth_tones"
                              # Custom: "jw_precip", "jw_temp", "fire", "ocean_depth"
                              # Original: "precipitation", "temperature", "precip_dif", "temp_dif"

# C) Map Range Settings
MAP_RANGE = {
    "from_min": 0,      # Minimum value in your data
    "from_max": 2,   # Maximum value in your data
    "to_min": 0.0,      # Maps to color ramp start
    "to_max": 1.0       # Maps to color ramp end
}

# D) Overlay
COLORBAR_OVERLAY = True  # Create composite images with colorbars
OVERLAY_SETTINGS = {
    "position": "top_right",        # Colorbar position
    "colorbar_text": "black",       # Text color
    "colorbar_scale": 0.4,          # Scale relative to image height
    "colorbar_steps": 6,            # Number of tick marks
    "padding": 50,                  # Padding from edges
    "background_opacity": 0.0       # Background transparency
}

# E) Plot Type and Styling
WOW_MODE = True  # Glossy surface, emission glow, displacement, adds "_wow" to filenames
RENDER_OBJECT = "robinson"  # Options: "sphere" or "robinson"

# F) SPHERE OPTIONS
TESTING_MODE = True
TEST_CAMERA = "Europe"  # Which camera to render in testing mode

ROTATION_OFFSET = {
    "x": 0.0,
    "y": 0.0,
    "z": 90  # Use 90 for uncentered input files, 180 for Pacific-centered maps
}

# Camera Settings
CAMERA_SETTINGS = {
    "focal_length": 50,           # mm - base focal length
    "zoom_level": 0.5,            # 0 = full sphere visible, 0.5 = close zoom
    "distance": 6,                # Distance from sphere center
    "depth_of_field": False,       # Enable/disable depth of field effect
    "aperture_fstop": 0.7         # F-stop value (lower = more blur)
}

# Continent camera positions (lat, lon in degrees)
CONTINENT_POSITIONS = {
    "Africa": (0, 20),           
    "Europe": (50, 10),          
    "Asia": (30, 90),            
    "North_America": (45, -100), 
    "South_America": (-15, -60), 
    "Australia": (-25, 135),     
    "Arctic": (75, 0),           
    "Antarctica": (-90, 0)       
}

# Interest point camera positions (lat, lon in degrees)
INTEREST_POSITIONS = {
    "Marrakech_Atlas": (31.6, -8.0),     # Marrakech-Atlas Mountains
    "Congo_River": (0, 18),              # Congo River basin
    "Himalayas": (28, 87)                # Himalayas region
}

# G) Robinson-specific settings
ROBINSON_SETTINGS = {
    "aspect_ratio": "4:2",      # 4:2 aspect ratio for Robinson
    "resolution_width": 4000,   # Width in pixels
    "alpha_mask": "robinson_mask.tif"  # Alpha mask filename
}

# ==============================================================================
# COLORMAP LOADING SYSTEM
# ==============================================================================

def load_colormap_library():
    """Load the external colormap library"""
    try:
        # Get the directory where the main script is located
        script_dir = os.path.dirname(bpy.data.filepath)
        if not script_dir:
            # If running in Blender without saved file, try current directory
            script_dir = os.getcwd()
        
        # Look for colormap_library.py in the same directory
        colormap_file = os.path.join(script_dir, "colormap_library.py")
        
        if not os.path.exists(colormap_file):
            print(f"Warning: colormap_library.py not found at {colormap_file}")
            print("Using fallback colormaps only.")
            return None
        
        # Add script directory to Python path if not already there
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        
        # Import the colormap library
        import colormap_library
        print(f"✓ Colormap library loaded from: {colormap_file}")
        
        return colormap_library
        
    except ImportError as e:
        print(f"Error importing colormap library: {e}")
        return None
    except Exception as e:
        print(f"Error loading colormap library: {e}")
        return None

def srgb_to_linear(srgb_value):
    """Convert sRGB color value to linear RGB"""
    if srgb_value <= 0.04045:
        return srgb_value / 12.92
    else:
        return pow((srgb_value + 0.055) / 1.055, 2.4)

def matplotlib_to_blender_colormap(colormap_name, num_samples=20):
    """Convert a matplotlib colormap to Blender color ramp format with proper color space conversion"""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        cmap = plt.get_cmap(colormap_name)
        positions = np.linspace(0, 1, num_samples)
        colors = []
        
        for pos in positions:
            rgba_srgb = cmap(pos)
            r_linear = srgb_to_linear(rgba_srgb[0])
            g_linear = srgb_to_linear(rgba_srgb[1])
            b_linear = srgb_to_linear(rgba_srgb[2])
            a_linear = rgba_srgb[3]
            colors.append((pos, [r_linear, g_linear, b_linear, a_linear]))
        
        print(f"✓ Converted matplotlib colormap '{colormap_name}' from sRGB to linear RGB")
        return colors
        
    except ImportError:
        print(f"Warning: matplotlib not available, cannot load colormap '{colormap_name}'")
        return [(0.0, [0.0, 0.0, 0.0, 1.0]), (1.0, [1.0, 1.0, 1.0, 1.0])]
    except Exception as e:
        print(f"Error loading matplotlib colormap '{colormap_name}': {e}")
        return [(0.0, [0.0, 0.0, 0.0, 1.0]), (1.0, [1.0, 1.0, 1.0, 1.0])]

def get_colormap_data(colormap_name, colormap_lib=None):
    """Get colormap data for the specified colormap name"""
    
    if colormap_lib is None:
        # Fallback to basic colormaps if library not available
        return get_fallback_colormap(colormap_name)
    
    try:
        # Check if it's a custom colormap
        if colormap_lib.is_custom_colormap(colormap_name):
            print(f"Using custom colormap: {colormap_name}")
            return colormap_lib.get_custom_colormap(colormap_name)
        
        # Check if it's a matplotlib colormap
        elif colormap_lib.is_matplotlib_colormap(colormap_name):
            print(f"Using matplotlib colormap: {colormap_name}")
            return matplotlib_to_blender_colormap(colormap_name, num_samples=20)
        
        else:
            print(f"Warning: Colormap '{colormap_name}' not found in library")
            # Use fallback
            return get_fallback_colormap(colormap_name)
            
    except Exception as e:
        print(f"Error loading colormap '{colormap_name}': {e}")
        return get_fallback_colormap(colormap_name)

def get_fallback_colormap(colormap_name):
    """Provide basic fallback colormaps if library is not available"""
    
    # Helper function to convert sRGB to linear
    def srgb_to_linear(srgb_value):
        if srgb_value <= 0.04045:
            return srgb_value / 12.92
        else:
            return pow((srgb_value + 0.055) / 1.055, 2.4)
    
    # Convert sRGB colors to linear RGB
    def convert_color(srgb_color):
        return [srgb_to_linear(srgb_color[0]), srgb_to_linear(srgb_color[1]), srgb_to_linear(srgb_color[2]), srgb_color[3]]
    
    # Define fallback maps in sRGB first, then convert
    fallback_maps_srgb = {
        "temperature": [
            (0.0, [0.0, 0.0, 0.5, 1.0]),    # Blue (cold)
            (0.5, [0.5, 0.5, 0.5, 1.0]),    # Gray (neutral)
            (1.0, [0.8, 0.2, 0.2, 1.0])     # Red (hot)
        ],
        "precipitation": [
            (0.0, [0.8, 0.7, 0.5, 1.0]),    # Tan (dry)
            (0.5, [0.4, 0.7, 0.4, 1.0]),    # Green (moderate)
            (1.0, [0.2, 0.3, 0.8, 1.0])     # Blue (wet)
        ],
        "viridis": [  # Approximate viridis colors in sRGB
            (0.0, [0.27, 0.00, 0.33, 1.0]),
            (0.25, [0.23, 0.30, 0.55, 1.0]),
            (0.5, [0.13, 0.57, 0.55, 1.0]),
            (0.75, [0.37, 0.80, 0.39, 1.0]),
            (1.0, [0.99, 0.91, 0.15, 1.0])
        ],
        "plasma": [  # Approximate plasma colors in sRGB
            (0.0, [0.05, 0.03, 0.53, 1.0]),
            (0.25, [0.5, 0.0, 0.7, 1.0]),
            (0.5, [0.8, 0.3, 0.4, 1.0]),
            (0.75, [0.95, 0.7, 0.2, 1.0]),
            (1.0, [0.95, 0.95, 0.1, 1.0])
        ]
    }
    
    if colormap_name in fallback_maps_srgb:
        # Convert sRGB fallback to linear RGB
        srgb_colors = fallback_maps_srgb[colormap_name]
        linear_colors = []
        for pos, color in srgb_colors:
            linear_color = convert_color(color)
            linear_colors.append((pos, linear_color))
        
        print(f"Using fallback colormap for: {colormap_name} (converted to linear RGB)")
        return linear_colors
    else:
        print(f"Warning: No fallback available for '{colormap_name}', using grayscale")
        # Grayscale fallback (already in linear RGB)
        return [
            (0.0, [0.0, 0.0, 0.0, 1.0]),    # Black
            (1.0, [1.0, 1.0, 1.0, 1.0])     # White
        ]

# ==============================================================================
# MAIN SCRIPT FUNCTIONS
# ==============================================================================

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def find_geotiff(projection="EPSG:4326"):
    """Find GeoTIFF in projection-specific folder"""
    # If specific path is provided, use it
    if GEOTIFF_PATH and os.path.exists(GEOTIFF_PATH):
        filename = os.path.splitext(os.path.basename(GEOTIFF_PATH))[0]
        return GEOTIFF_PATH, filename
    
    script_dir = os.path.dirname(bpy.data.filepath)
    data_sphere_dir = os.path.dirname(script_dir)
    
    # Look in projection-specific folder
    if projection == "ESRI:54030":
        input_dir = os.path.join(data_sphere_dir, "Input", "ESRI:54030")
        print(f"Looking for Robinson GeoTIFF in: Input/ESRI:54030/")
    else:
        input_dir = os.path.join(data_sphere_dir, "Input", "EPSG:4326")
        print(f"Looking for Plate Carrée GeoTIFF in: Input/EPSG:4326/")
    
    if not os.path.exists(input_dir):
        print(f"Creating directory: {input_dir}")
        os.makedirs(input_dir, exist_ok=True)
        return None, None
    
    tiff_files = []
    for pattern in ["*.tif", "*.tiff", "*.TIF", "*.TIFF"]:
        found_files = glob.glob(os.path.join(input_dir, pattern))
        # For Robinson, exclude mask files
        if projection == "ESRI:54030":
            tiff_files.extend([f for f in found_files if 'mask' not in os.path.basename(f).lower()])
        else:
            tiff_files.extend(found_files)
    
    if tiff_files:
        print(f"Found {len(tiff_files)} GeoTIFF files:")
        for i, file in enumerate(tiff_files):
            print(f"  {i+1}: {os.path.basename(file)}")
        
        selected_file = tiff_files[0]
        filename = os.path.splitext(os.path.basename(selected_file))[0]
        print(f"Using: {os.path.basename(selected_file)}")
        return selected_file, filename
    else:
        print(f"No GeoTIFF files found in {projection} folder")
        return None, None

def create_sphere():
    """Create sphere with subdivision"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0))
    sphere = bpy.context.active_object
    sphere.name = "climate_sphere"
    sphere.scale = (2, 2, 2)
    
    subdivision = sphere.modifiers.new(name="Subdivision", type='SUBSURF')
    subdivision.levels = 3
    subdivision.render_levels = 6
    
    bpy.ops.object.shade_smooth()
    print("Sphere created with subdivision")
    return sphere

def create_robinson_plane():
    """Create Robinson projection plane"""
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
    robinson = bpy.context.active_object
    robinson.name = "robinson_projection"
    
    # Scale to 4:2 aspect ratio (Robinson projection proportions)
    robinson.scale = (2, 1, 1)
    
    # Enter edit mode and subdivide the mesh
    bpy.context.view_layer.objects.active = robinson
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Subdivide the plane mesh 4 times
    for _ in range(4):
        bpy.ops.mesh.subdivide()
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Add subdivision surface modifier
    subdivision = robinson.modifiers.new(name="Subdivision", type='SUBSURF')
    subdivision.subdivision_type = 'SIMPLE'  # Use simple subdivision
    subdivision.levels = 3                   # Viewport subdivision
    subdivision.render_levels = 3            # Render subdivision
    
    bpy.ops.object.shade_smooth()
    print(f"Robinson plane created with 4x mesh subdivision + simple subsurf (4:2 aspect ratio)")
    return robinson

def setup_color_ramp(color_ramp_node, colormap_name, colormap_lib=None):
    """Set up color ramp based on colormap name (custom or matplotlib)"""
    
    # Get the colormap data
    colors = get_colormap_data(colormap_name, colormap_lib)
    
    if not colors:
        print(f"Error: Could not load colormap '{colormap_name}'")
        return
    
    color_ramp = color_ramp_node.color_ramp
    
    # Clear existing elements except first and last
    while len(color_ramp.elements) > 2:
        color_ramp.elements.remove(color_ramp.elements[0])
    
    # Set first and last elements
    color_ramp.elements[0].position = colors[0][0]
    color_ramp.elements[0].color = colors[0][1]
    color_ramp.elements[1].position = colors[-1][0]  
    color_ramp.elements[1].color = colors[-1][1]
    
    # Add intermediate colors
    for pos, color in colors[1:-1]:
        element = color_ramp.elements.new(pos)
        element.color = color
    
    print(f"✓ Colormap '{colormap_name}' applied with {len(colors)} color stops")

def create_climate_material(obj, geotiff_path, is_robinson=False, colormap_lib=None):
    """Create climate material - works for both sphere and Robinson"""
    material_name = "robinson_material" if is_robinson else "climate_material"
    mat = bpy.data.materials.new(name=material_name)
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    print(f"Creating {'Robinson' if is_robinson else 'sphere'} material for colormap: {DISPLAY_COLOR}")
    
    # Main nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 300)
    
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (-236.5, 430)
    principled.inputs['Roughness'].default_value = 0.6 if WOW_MODE else 0.95
    
    # Texture nodes
    if is_robinson:
        # Robinson uses Image Texture (not Environment Texture)
        tex_coord = nodes.new(type='ShaderNodeTexCoord')
        tex_coord.location = (-2852.8, 117.1)
        
        image_tex = nodes.new(type='ShaderNodeTexImage')
        image_tex.location = (-2318.3, 57.9)
        image_tex.label = "Robinson Data"
    else:
        # Sphere uses Environment Texture
        tex_coord = nodes.new(type='ShaderNodeTexCoord')
        tex_coord.location = (-2852.8, 117.1)
        
        mapping = nodes.new(type='ShaderNodeMapping')
        mapping.location = (-2649.5, 119.0)
        mapping.inputs['Scale'].default_value = (1.0, -1.0, 1.0)
        mapping.inputs['Rotation'].default_value = (
            math.radians(ROTATION_OFFSET['x']),
            math.radians(ROTATION_OFFSET['y']),
            math.radians(ROTATION_OFFSET['z'])
        )
        
        env_tex = nodes.new(type='ShaderNodeTexEnvironment')
        env_tex.location = (-2318.3, 57.9)
        env_tex.label = "Sphere Data"
    
    # Load main texture
    if geotiff_path and os.path.exists(geotiff_path):
        try:
            img = bpy.data.images.load(geotiff_path)
            if is_robinson:
                image_tex.image = img
            else:
                env_tex.image = img
            
            # Set to Non-Color for data
            try:
                img.colorspace_settings.name = 'Non-Color'
                print("Image colorspace set to Non-Color")
            except:
                try:
                    img.color_space = 'Non-Color'
                    print("Image colorspace set to Non-Color (legacy)")
                except:
                    print("Could not set colorspace")
            
            print(f"Texture loaded: {os.path.basename(geotiff_path)}")
        except Exception as e:
            print(f"⌧ Failed to load texture: {e}")
    
    # Alpha mask for Robinson
    alpha_tex = None
    if is_robinson:
        # Look for Robinson mask in same directory
        mask_path = os.path.join(os.path.dirname(geotiff_path), ROBINSON_SETTINGS["alpha_mask"])
        if os.path.exists(mask_path):
            try:
                alpha_tex = nodes.new(type='ShaderNodeTexImage')
                alpha_tex.location = (-2318.3, -300)
                alpha_tex.label = "Robinson Mask"
                
                mask_img = bpy.data.images.load(mask_path)
                alpha_tex.image = mask_img
                
                # Set mask to Non-Color
                try:
                    mask_img.colorspace_settings.name = 'Non-Color'
                except:
                    try:
                        mask_img.color_space = 'Non-Color'
                    except:
                        pass
                
                print(f"Robinson mask loaded: {ROBINSON_SETTINGS['alpha_mask']}")
            except Exception as e:
                print(f"Could not load Robinson mask: {e}")
        else:
            print(f"Robinson mask not found: {mask_path}")
    
    # Data processing nodes
    map_range = nodes.new(type='ShaderNodeMapRange')
    map_range.location = (-1854.1, 341.0)
    map_range.inputs['From Min'].default_value = MAP_RANGE['from_min']
    map_range.inputs['From Max'].default_value = MAP_RANGE['from_max']
    map_range.inputs['To Min'].default_value = MAP_RANGE['to_min']
    map_range.inputs['To Max'].default_value = MAP_RANGE['to_max']
    
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-1678.3, 633.2)
    color_ramp.width = 700
    color_ramp.label = DISPLAY_COLOR
    
    # Use the new colormap system instead of hardcoded ramps
    setup_color_ramp(color_ramp, DISPLAY_COLOR, colormap_lib)
    
    # Surface detail nodes
    bump = nodes.new(type='ShaderNodeBump')
    bump.location = (-664.4, 799.1)
    bump.inputs['Strength'].default_value = 0.3
    bump.inputs['Distance'].default_value = 3.0
    
    displacement = nodes.new(type='ShaderNodeDisplacement')
    displacement.location = (-692.5, -133.9)
    if WOW_MODE:
        displacement.inputs['Scale'].default_value = 0.02
        displacement.inputs['Midlevel'].default_value = 0.0
        math_power = nodes.new(type='ShaderNodeMath')
        math_power.location = (-400, 300)
        math_power.operation = 'POWER'
        math_power.inputs[1].default_value = 0.001
        math_power.label = "Emission Power"
    else:
        displacement.inputs['Scale'].default_value = 0.00
        displacement.inputs['Midlevel'].default_value = 0
    
    try:
        mat.displacement_method = 'BOTH'
    except:
        pass
    
    # Connections
    try:
        if is_robinson:
            # Robinson connections (Image Texture)
            links.new(tex_coord.outputs['UV'], image_tex.inputs['Vector'])
            links.new(image_tex.outputs['Color'], map_range.inputs['Value'])
            
            # Connect alpha mask if available
            if alpha_tex:
                links.new(tex_coord.outputs['UV'], alpha_tex.inputs['Vector'])
                links.new(alpha_tex.outputs['Color'], principled.inputs['Alpha'])
        else:
            # Sphere connections (Environment Texture)
            links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
            links.new(mapping.outputs['Vector'], env_tex.inputs['Vector'])
            links.new(env_tex.outputs['Color'], map_range.inputs['Value'])
        
        # Common connections
        links.new(map_range.outputs['Result'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
        links.new(color_ramp.outputs['Color'], principled.inputs['Emission Color'])
        
        if WOW_MODE:
            links.new(color_ramp.outputs['Color'], math_power.inputs[0])
            links.new(math_power.outputs['Value'], principled.inputs['Emission Strength'])
        else:
            principled.inputs['Emission Strength'].default_value = 1.0
        
        links.new(color_ramp.outputs['Color'], bump.inputs['Height'])
        links.new(bump.outputs['Normal'], principled.inputs['Normal'])
        links.new(color_ramp.outputs['Color'], displacement.inputs['Height'])
        links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        print("All material node connections complete")
        
    except Exception as e:
        print(f"Some material connections failed: {e}")
    
    return mat

def create_continent_cameras():
    """Create cameras for each continent and interest point"""
    cameras = {}
    distance = CAMERA_SETTINGS["distance"]
    focal_length = CAMERA_SETTINGS["focal_length"]
    zoom_level = CAMERA_SETTINGS["zoom_level"]
    use_dof = CAMERA_SETTINGS["depth_of_field"]
    aperture_fstop = CAMERA_SETTINGS["aperture_fstop"]
    
    adjusted_focal = focal_length * (1 + zoom_level)
    
    # Combine continent and interest positions
    all_positions = {**CONTINENT_POSITIONS, **INTEREST_POSITIONS}
    
    print(f"Creating {len(all_positions)} sphere cameras (focal length: {adjusted_focal}mm)")
    if use_dof or WOW_MODE:
        sphere_radius = 2.0
        focus_dist = distance - sphere_radius
        print(f"  DOF enabled (f/{aperture_fstop}, focus at sphere surface: {focus_dist} units)")
    
    for location_name, (lat, lon) in all_positions.items():
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        
        x = distance * math.cos(lat_rad) * math.sin(lon_rad)
        y = -distance * math.cos(lat_rad) * math.cos(lon_rad)
        z = distance * math.sin(lat_rad)
        
        bpy.ops.object.camera_add(location=(x, y, z))
        camera = bpy.context.active_object
        camera.name = f"Camera_Sphere_{location_name}"
        camera.data.lens = adjusted_focal
        
        if use_dof or WOW_MODE:
            camera.data.dof.use_dof = True
            sphere_radius = 2.0
            focus_dist = distance - sphere_radius
            camera.data.dof.focus_distance = focus_dist
            camera.data.dof.aperture_fstop = aperture_fstop
        else:
            camera.data.dof.use_dof = False
        
        direction = bpy.data.objects['climate_sphere'].location - camera.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        camera.rotation_euler = rot_quat.to_euler()
        
        cameras[location_name] = camera
        print(f"  {location_name}: position ({x:.2f}, {y:.2f}, {z:.2f})")
    
    return cameras

def create_robinson_camera():
    """Create top-view camera for Robinson projection"""
    # Position camera directly above, looking down
    bpy.ops.object.camera_add(location=(0, 0, 5))
    camera = bpy.context.active_object
    camera.name = "Camera_Robinson_TopView"
    
    # Point camera straight down
    camera.rotation_euler = (0, 0, 0)  # Top-down view
    
    # Set up for Robinson aspect ratio
    camera.data.lens = 50
    camera.data.type = 'ORTHO'  # Orthographic camera for flat map
    camera.data.ortho_scale = 4  # Adjust to frame the plane properly
    
    print(f"Robinson camera created (orthographic, top-down view)")
    
    return {"TopView": camera}

def setup_render_settings(obj_type="sphere"):
    """Configure render settings for sphere or Robinson"""
    scene = bpy.context.scene
    
    if obj_type == "robinson":
        # 4:2 aspect ratio for Robinson
        scene.render.resolution_x = ROBINSON_SETTINGS["resolution_width"]
        scene.render.resolution_y = ROBINSON_SETTINGS["resolution_width"] // 2
        print(f"Robinson render settings: {scene.render.resolution_x} x {scene.render.resolution_y}")
    else:
        # Square for sphere
        scene.render.resolution_x = 2000
        scene.render.resolution_y = 2000
        print(f"Sphere render settings: {scene.render.resolution_x} x {scene.render.resolution_y}")
    
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    scene.render.engine = 'CYCLES'
    
    if CAMERA_SETTINGS["depth_of_field"] or WOW_MODE:
        scene.cycles.samples = 256
        print("  High samples (256) for DOF/WOW mode")
    else:
        scene.cycles.samples = 128
        print("  Standard samples (128)")
    
    try:
        cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
        cycles_prefs.compute_device_type = 'CUDA'
        scene.cycles.device = 'GPU'
        print("GPU rendering enabled")
    except:
        scene.cycles.device = 'CPU'
        print("Using CPU rendering")

def add_lighting():
    """Add appropriate lighting based on render mode"""
    if RENDER_OBJECT == "sphere":
        if WOW_MODE:
            # Dual sun lights for sphere in WOW mode
            bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
            sun1 = bpy.context.active_object
            sun1.name = "sun_light_1"
            sun1.data.energy = 0.5
            sun1.data.angle = math.radians(65)
            
            bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
            sun2 = bpy.context.active_object
            sun2.name = "sun_light_2"
            sun2.data.energy = 0.5
            sun2.data.angle = math.radians(65)
            sun2.rotation_euler[1] = math.radians(180)
            
            print("Dual sun lights added for sphere (WOW mode)")
        else:
            # Single sun light for sphere
            bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
            sun = bpy.context.active_object
            sun.name = "sun_light"
            sun.data.energy = 0.5
            print("Single sun light added for sphere")
    
    elif RENDER_OBJECT == "robinson":
        if WOW_MODE:
            # Only displacement light for Robinson in WOW mode
            bpy.ops.object.light_add(type='SUN', location=(8, 2, 4))
            displacement_light = bpy.context.active_object
            displacement_light.name = "robinson_displacement_light"
            displacement_light.data.energy = 0.5  # Full strength
            displacement_light.data.angle = math.radians(30)  # Sharp angle for displacement shadows
            # Point light slightly from the side to catch displacement details
            displacement_light.rotation_euler = (math.radians(45), math.radians(20), 0)
            
            print("Robinson displacement light (WOW mode)")
        else:
            # No lighting in standard mode - rely on world/environment lighting
            print("Robinson lighting (standard - using world light)")

def format_range_value(value):
    if value >= 0:
        return f"+{value:g}"
    else:
        return f"{value:g}"

def ensure_matplotlib():
    try:
        import matplotlib
        return True
    except ImportError:
        try:
            import subprocess
            import sys
            import os
            
            if sys.platform == "win32":
                python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
            else:
                python_exe = os.path.join(sys.prefix, 'bin', 'python3')
            
            result = subprocess.call([
                python_exe, '-m', 'pip', 'install', 
                'matplotlib', '--user'
            ])
            
            if result == 0:
                try:
                    import matplotlib
                    return True
                except ImportError:
                    return False
            else:
                return False
        except Exception:
            return False

def ensure_pil():
    try:
        from PIL import Image, ImageEnhance
        return True
    except ImportError:
        try:
            import subprocess
            import sys
            import os
            
            if sys.platform == "win32":
                python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
            else:
                python_exe = os.path.join(sys.prefix, 'bin', 'python3')
            
            result = subprocess.call([
                python_exe, '-m', 'pip', 'install', 
                'Pillow', '--user'
            ])
            
            if result == 0:
                try:
                    from PIL import Image, ImageEnhance
                    return True
                except ImportError:
                    return False
            else:
                return False
        except Exception:
            return False

def create_colorbar_overlay(sphere_image_path, colorbar_image_path, output_path, input_filename=None):
    if not ensure_pil():
        return False
    
    try:
        from PIL import Image, ImageEnhance, ImageDraw, ImageFont
        
        try:
            sphere_img = Image.open(sphere_image_path).convert('RGBA')
            colorbar_img = Image.open(colorbar_image_path).convert('RGBA')
        except FileNotFoundError:
            return False
        
        sphere_width, sphere_height = sphere_img.size
        colorbar_width, colorbar_height = colorbar_img.size
        
        scale_factor = OVERLAY_SETTINGS["colorbar_scale"]
        new_colorbar_height = int(sphere_height * scale_factor)
        scale_ratio = new_colorbar_height / colorbar_height
        new_colorbar_width = int(colorbar_width * scale_ratio)
        
        colorbar_resized = colorbar_img.resize((new_colorbar_width, new_colorbar_height), Image.Resampling.LANCZOS)
        
        if OVERLAY_SETTINGS["background_opacity"] > 0:
            bg_padding = 10
            bg_width = new_colorbar_width + (bg_padding * 2)
            bg_height = new_colorbar_height + (bg_padding * 2)
            bg_alpha = int(255 * OVERLAY_SETTINGS["background_opacity"])
            
            background = Image.new('RGBA', (bg_width, bg_height), (0, 0, 0, bg_alpha))
            bg_x = bg_padding
            bg_y = bg_padding
            background.paste(colorbar_resized, (bg_x, bg_y), colorbar_resized)
            colorbar_final = background
        else:
            colorbar_final = colorbar_resized
        
        padding = OVERLAY_SETTINGS["padding"]
        position = OVERLAY_SETTINGS["position"]
        final_colorbar_width, final_colorbar_height = colorbar_final.size
        
        if position == "top_right":
            x = sphere_width - final_colorbar_width - padding
            y = padding
        elif position == "top_left":
            x = padding
            y = padding
        elif position == "bottom_right":
            x = sphere_width - final_colorbar_width - padding
            y = sphere_height - final_colorbar_height - padding
        elif position == "bottom_left":
            x = padding
            y = sphere_height - final_colorbar_height - padding
        else:
            x = sphere_width - final_colorbar_width - padding
            y = padding
        
        x = max(0, min(x, sphere_width - final_colorbar_width))
        y = max(0, min(y, sphere_height - final_colorbar_height))
        
        composite = sphere_img.copy()
        composite.paste(colorbar_final, (x, y), colorbar_final)
        
        if input_filename:
            filename_prefix = input_filename.split('_')[0]
            draw = ImageDraw.Draw(composite)
            
            text_color = OVERLAY_SETTINGS["colorbar_text"]
            if text_color == "auto":
                text_color = "white" if WOW_MODE else "black"
            
            if text_color == "white":
                color_rgb = (255, 255, 255, 255)
            else:
                color_rgb = (0, 0, 0, 255)
            
            try:
                font_size = max(24, int(sphere_height * 0.025))
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
                except:
                    try:
                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
            
            text_padding = 30
            bbox = draw.textbbox((0, 0), filename_prefix, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            text_x = sphere_width - text_width - text_padding
            text_y = sphere_height - text_height - text_padding
            
            draw.text((text_x, text_y), filename_prefix, fill=color_rgb, font=font)
        
        composite.save(output_path, 'PNG')
        
        sphere_img.close()
        colorbar_img.close()
        colorbar_resized.close()
        if 'background' in locals():
            background.close()
        colorbar_final.close()
        composite.close()
        
        return True
        
    except Exception:
        return False

def generate_scientific_colorbars(output_dir, variable_type, from_min, from_max, suffix="", colormap_lib=None):
    """Generate colorbars using the new colormap system"""
    if not ensure_matplotlib():
        return
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        import numpy as np
        
        plt.ioff()
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except OSError:
                import tempfile
                output_dir = tempfile.gettempdir()
        
        test_file = os.path.join(output_dir, "test_write_permissions.tmp")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
        except OSError:
            import tempfile
            output_dir = tempfile.gettempdir()
        
        # Create colormap for matplotlib
        if colormap_lib and hasattr(colormap_lib, 'is_matplotlib_colormap') and colormap_lib.is_matplotlib_colormap(variable_type):
            # Use matplotlib colormap directly
            try:
                cmap = plt.get_cmap(variable_type)
                print(f"Using matplotlib colormap directly: {variable_type}")
            except:
                # Fallback to manual creation
                colors_data = get_colormap_data(variable_type, colormap_lib)
                positions = [item[0] for item in colors_data]
                colors = [item[1][:3] for item in colors_data]  # RGB only
                cmap = mcolors.LinearSegmentedColormap.from_list(variable_type, list(zip(positions, colors)))
                print(f"Created matplotlib colormap from library data: {variable_type}")
        else:
            # Create from custom colormap data
            colors_data = get_colormap_data(variable_type, colormap_lib)
            if colors_data:
                positions = [item[0] for item in colors_data]
                colors = [item[1][:3] for item in colors_data]  # RGB only
                cmap = mcolors.LinearSegmentedColormap.from_list(variable_type, list(zip(positions, colors)))
                print(f"Created matplotlib colormap from custom data: {variable_type}")
            else:
                print(f"Warning: Could not create colormap for {variable_type}")
                return
        
        for text_color in ['black', 'white']:
            try:
                fig, ax = plt.subplots(figsize=(2, 4.8))  
                fig.patch.set_alpha(0.0)
                ax.set_facecolor('none')
                
                norm = mcolors.Normalize(vmin=from_min, vmax=from_max)
                cbar = fig.colorbar(
                    plt.cm.ScalarMappable(norm=norm, cmap=cmap),
                    ax=ax,
                    fraction=0.8,
                    pad=0.1
                )
                
                cbar.ax.tick_params(
                    colors=text_color, 
                    labelsize=14,
                    width=2,
                    length=6
                )
                cbar.outline.set_edgecolor(text_color)
                cbar.outline.set_linewidth(2)
                
                num_ticks = OVERLAY_SETTINGS["colorbar_steps"]
                tick_values = np.linspace(from_min, from_max, num_ticks)
                cbar.set_ticks(tick_values)
                cbar.set_ticklabels([f'{val:.1f}' for val in tick_values])
                
                ax.remove()
                
                from_min_str = format_range_value(from_min)
                from_max_str = format_range_value(from_max)
                filename = f"{variable_type}_colorbar{suffix}_{from_min_str}_{from_max_str}_{text_color}.png"
                filepath = os.path.join(output_dir, filename)
                
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                plt.savefig(
                    filepath,
                    dpi=300,
                    bbox_inches='tight',
                    transparent=True,
                    pad_inches=0.1,
                    facecolor='none'
                )
                
            except Exception:
                try:
                    import tempfile
                    alt_filepath = os.path.join(tempfile.gettempdir(), filename)
                    
                    plt.savefig(
                        alt_filepath,
                        dpi=300,
                        bbox_inches='tight',
                        transparent=True,
                        pad_inches=0.1,
                        facecolor='none'
                    )
                except Exception:
                    pass
            
            finally:
                try:
                    plt.close(fig)
                except:
                    pass
        
        plt.close('all')
        
        try:
            plt.clf()
            plt.cla()
        except:
            pass
        
    except Exception:
        pass
    
    finally:
        try:
            import gc
            gc.collect()
            
            if 'matplotlib.pyplot' in globals():
                plt.close('all')
        except:
            pass

def create_overlays_for_renders(output_dir, input_filename, suffix, obj_type):
    if not COLORBAR_OVERLAY:
        return
    
    colorbar_text = OVERLAY_SETTINGS["colorbar_text"]
    if colorbar_text == "auto":
        colorbar_text = "white" if WOW_MODE else "black"
    
    from_min_str = format_range_value(MAP_RANGE['from_min'])
    from_max_str = format_range_value(MAP_RANGE['from_max'])
    colorbar_filename = f"{DISPLAY_COLOR}_colorbar{suffix}_{from_min_str}_{from_max_str}_{colorbar_text}.png"
    colorbar_path = os.path.join(output_dir, colorbar_filename)
    
    if not os.path.exists(colorbar_path):
        print(f"Colorbar not found: {colorbar_path}")
        return
    
    # Find rendered files to overlay
    rendered_files = []
    
    if TESTING_MODE:
        if obj_type == "robinson":
            # Robinson testing mode
            if input_filename:
                test_filename = f"{input_filename}_TopView{suffix}.png"
            else:
                test_filename = f"test_TopView{suffix}.png"
        else:
            # Sphere testing mode  
            if input_filename:
                test_filename = f"{input_filename}_{TEST_CAMERA}{suffix}.png"
            else:
                test_filename = f"test_{TEST_CAMERA}{suffix}.png"
        
        test_path = os.path.join(output_dir, test_filename)
        if os.path.exists(test_path):
            rendered_files.append(test_filename)
            print(f"Found test file for overlay: {test_filename}")
        else:
            print(f"Test file not found for overlay: {test_filename}")
    
    else:
        # Normal mode - find all rendered files
        if obj_type == "sphere":
            # All continent and interest positions
            all_positions = {**CONTINENT_POSITIONS, **INTEREST_POSITIONS}
            for location_name in all_positions.keys():
                if input_filename:
                    filename = f"{input_filename}_{location_name}{suffix}.png"
                else:
                    filename = f"sphere_{location_name}{suffix}.png"
                
                if os.path.exists(os.path.join(output_dir, filename)):
                    rendered_files.append(filename)
        
        else:  # robinson
            # Robinson has only TopView camera
            if input_filename:
                filename = f"{input_filename}_TopView{suffix}.png"
            else:
                filename = f"robinson_TopView{suffix}.png"
            
            filepath = os.path.join(output_dir, filename)
            if os.path.exists(filepath):
                rendered_files.append(filename)
                print(f"Found Robinson file for overlay: {filename}")
            else:
                print(f"Robinson file not found for overlay: {filename}")
    
    if not rendered_files:
        print(f"No rendered files found for {obj_type} overlay")
        return
    
    success_count = 0
    for rendered_filename in rendered_files:
        rendered_path = os.path.join(output_dir, rendered_filename)
        base_name = rendered_filename.replace('.png', '')
        composite_filename = f"{base_name}_colorbar.png"
        composite_path = os.path.join(output_dir, composite_filename)
        
        print(f"Creating overlay: {rendered_filename} + colorbar -> {composite_filename}")
        
        if create_colorbar_overlay(rendered_path, colorbar_path, composite_path, input_filename):
            success_count += 1
            print(f"  Success: {composite_filename}")
        else:
            print(f"  Failed: {composite_filename}")
    
    print(f"Created {success_count}/{len(rendered_files)} overlay composites for {obj_type}")

def render_object_cameras(cameras, input_filename, obj_type="sphere", colormap_lib=None):
    """Render views from cameras"""
    script_dir = os.path.dirname(bpy.data.filepath)
    data_sphere_dir = os.path.dirname(script_dir)
    
    # Create proper output directory based on object type
    if obj_type == "robinson":
        output_dir = os.path.join(data_sphere_dir, "Output", "Robinson")
    else:
        output_dir = os.path.join(data_sphere_dir, "Output", "Sphere")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Build filename suffix
    suffix = ""
    if WOW_MODE:
        suffix += "_wow"
    
    zoom_val = CAMERA_SETTINGS['zoom_level']
    if zoom_val == int(zoom_val):
        zoom_str = f"{int(zoom_val):02d}"
    else:
        zoom_str = f"{zoom_val:.2f}".replace('.', '')
    suffix += f"_zoom{zoom_str}"
    
    if CAMERA_SETTINGS["depth_of_field"]:
        fstop_str = f"{CAMERA_SETTINGS['aperture_fstop']:.1f}".replace('.', '')
        suffix += f"_dof_f{fstop_str}"
    
    from_min_str = format_range_value(MAP_RANGE['from_min'])
    from_max_str = format_range_value(MAP_RANGE['from_max'])
    suffix += f"_{from_min_str}_{from_max_str}"
    
    # Add object type to suffix
    if obj_type == "robinson":
        suffix += "_robinson"
    
    print(f"  Filename suffix: {suffix}")
    
    if TESTING_MODE:
        # In testing mode, only render one camera
        if obj_type == "robinson":
            # Robinson only has TopView camera
            if "TopView" in cameras:
                camera = cameras["TopView"]
                bpy.context.scene.camera = camera
                
                if input_filename:
                    output_name = f"{input_filename}_TopView{suffix}.png"
                else:
                    output_name = f"test_TopView{suffix}.png"
                
                output_path = os.path.join(output_dir, output_name)
                bpy.context.scene.render.filepath = output_path
                
                print(f"TESTING MODE: Rendering {obj_type} TopView...")
                print(f"  Output: {output_name}")
                
                try:
                    bpy.ops.render.render(write_still=True)
                    print(f"  Rendered: {output_path}")
                except Exception as e:
                    print(f"  Render failed: {e}")
            else:
                print(f"TopView camera not found!")
        else:
            # Sphere mode - render test camera
            if TEST_CAMERA in cameras:
                camera = cameras[TEST_CAMERA]
                bpy.context.scene.camera = camera
                
                if input_filename:
                    output_name = f"{input_filename}_{TEST_CAMERA}{suffix}.png"
                else:
                    output_name = f"test_{TEST_CAMERA}{suffix}.png"
                
                output_path = os.path.join(output_dir, output_name)
                bpy.context.scene.render.filepath = output_path
                
                print(f"TESTING MODE: Rendering {obj_type} {TEST_CAMERA} view only...")
                print(f"  Output: {output_name}")
                
                try:
                    bpy.ops.render.render(write_still=True)
                    print(f"  Rendered: {output_path}")
                except Exception as e:
                    print(f"  Render failed: {e}")
            else:
                print(f"Test camera '{TEST_CAMERA}' not found!")
    else:
        # Normal mode: render all cameras
        print(f"Rendering all {obj_type} views...")
        if WOW_MODE:
            print("  WOW MODE active - renders will take longer due to enhanced effects")
        
        for location_name, camera in cameras.items():
            bpy.context.scene.camera = camera
            
            if input_filename:
                output_name = f"{input_filename}_{location_name}{suffix}.png"
            else:
                output_name = f"{obj_type}_{location_name}{suffix}.png"
            
            output_path = os.path.join(output_dir, output_name)
            bpy.context.scene.render.filepath = output_path
            
            print(f"  Rendering {location_name}...")
            
            try:
                bpy.ops.render.render(write_still=True)
                print(f"  Saved: {output_name}")
            except Exception as e:
                print(f"  Failed: {e}")
        
        print(f"All {obj_type} renders complete! Check: {output_dir}")
    
    # Generate colorbars and overlays
    if COLORBAR_OVERLAY:
        print("Generating colorbars and overlays...")
        generate_scientific_colorbars(
            output_dir, 
            DISPLAY_COLOR,  # Changed from DISPLAY_VARIABLE
            MAP_RANGE['from_min'], 
            MAP_RANGE['from_max'], 
            suffix,
            colormap_lib    # Pass the colormap library
        )
        create_overlays_for_renders(output_dir, input_filename, suffix, obj_type)

def print_configuration():
    """Print current configuration with colormap info"""
    print("\n" + "="*70)
    print("CLIMATE GLOBE GENERATOR - ENHANCED CONFIGURATION")
    print("="*70)
    print(f"Colormap: {DISPLAY_COLOR}")  # Changed from Variable Type
    print(f"WOW MODE: {'ENABLED' if WOW_MODE else 'Disabled'}")
    if WOW_MODE:
        print("  - Enhanced visuals: DOF, glossy surface, emission glow, displacement light")
    print(f"COLORBAR OVERLAY: {'ENABLED' if COLORBAR_OVERLAY else 'Disabled'}")
    print(f"Map Range: [{MAP_RANGE['from_min']:.2f}, {MAP_RANGE['from_max']:.2f}] -> [{MAP_RANGE['to_min']:.2f}, {MAP_RANGE['to_max']:.2f}]")
    print(f"Camera DOF: {'ENABLED' if CAMERA_SETTINGS['depth_of_field'] else 'Disabled'}")
    if CAMERA_SETTINGS['depth_of_field']:
        print(f"  - Aperture: f/{CAMERA_SETTINGS['aperture_fstop']}")
    
    print(f"\nOBJECT SELECTION:")
    print(f"  - Render Mode: {RENDER_OBJECT.upper()}")
    
    if RENDER_OBJECT == "sphere":
        total_sphere_cameras = len(CONTINENT_POSITIONS) + len(INTEREST_POSITIONS)
        print(f"  - Sphere Cameras: {total_sphere_cameras} ({len(CONTINENT_POSITIONS)} continents + {len(INTEREST_POSITIONS)} interest points)")
    elif RENDER_OBJECT == "robinson":
        print(f"  - Robinson Camera: 1 (orthographic top-view, perfect fit)")
        print(f"  - Robinson Resolution: {ROBINSON_SETTINGS['resolution_width']} x {ROBINSON_SETTINGS['resolution_width']//2}")
        print(f"  - Robinson Mesh: 4x subdivision + simple subsurf (viewport: 3, render: 3)")
    
    if RENDER_OBJECT == "robinson":
        test_camera_display = "TopView" if TESTING_MODE else "N/A"
    else:
        test_camera_display = TEST_CAMERA
    
    print(f"Testing Mode: {TESTING_MODE} ({test_camera_display})")
    print("="*70 + "\n")

def main():
    """Enhanced main function with flexible colormap system"""
    print("CLIMATE GLOBE GENERATOR - ENHANCED WITH FLEXIBLE COLORMAPS")
    
    # Load colormap library first
    print("Loading colormap library...")
    colormap_lib = load_colormap_library()
    
    print_configuration()
    
    # 1. Clear scene
    print("1. Clearing scene...")
    clear_scene()
    
    # 2. Add lighting
    print("2. Adding lighting...")
    add_lighting()
    
    # 3. Create object based on selection
    if RENDER_OBJECT == "sphere":
        print("3. Creating SPHERE...")
        
        geotiff_path, input_filename = find_geotiff("EPSG:4326")
        if not geotiff_path:
            print("Warning: No sphere GeoTIFF found, continuing with procedural colors only")
        
        sphere = create_sphere()
        sphere_material = create_climate_material(sphere, geotiff_path, is_robinson=False, colormap_lib=colormap_lib)
        cameras = create_continent_cameras()
        
        print(f"Sphere setup complete ({len(cameras)} cameras)")
        
        # 4. Setup render settings and render
        print("4. Rendering SPHERE...")
        setup_render_settings("sphere")
        render_object_cameras(cameras, input_filename, "sphere", colormap_lib)
        
    elif RENDER_OBJECT == "robinson":
        print("3. Creating ROBINSON...")
        
        robinson_geotiff_path, robinson_filename = find_geotiff("ESRI:54030")
        if not robinson_geotiff_path:
            print("Warning: No Robinson GeoTIFF found, continuing with procedural colors only")
        
        robinson = create_robinson_plane()
        robinson_material = create_climate_material(robinson, robinson_geotiff_path, is_robinson=True, colormap_lib=colormap_lib)
        cameras = create_robinson_camera()
        
        print(f"Robinson setup complete (1 camera)")
        
        # 4. Setup render settings and render
        print("4. Rendering ROBINSON...")
        setup_render_settings("robinson")
        render_object_cameras(cameras, robinson_filename, "robinson", colormap_lib)
    
    else:
        print(f"ERROR: Invalid RENDER_OBJECT '{RENDER_OBJECT}'. Use 'sphere' or 'robinson'")
        return
    
    # 5. Final summary
    print("\n" + "="*70)
    print("CLIMATE GLOBE GENERATION COMPLETE!")
    print("="*70)
    print(f"✓ Colormap used: {DISPLAY_COLOR}")
    
    if colormap_lib:
        if hasattr(colormap_lib, 'is_custom_colormap') and colormap_lib.is_custom_colormap(DISPLAY_COLOR):
            print("  - Type: Custom colormap")
        elif hasattr(colormap_lib, 'is_matplotlib_colormap') and colormap_lib.is_matplotlib_colormap(DISPLAY_COLOR):
            print("  - Type: Matplotlib colormap") 
        else:
            print("  - Type: Fallback colormap")
    else:
        print("  - Type: Fallback colormap (library not loaded)")
    
    if RENDER_OBJECT == "sphere":
        if 'input_filename' in locals() and input_filename:
            print(f"SPHERE: {os.path.basename(input_filename)}")
        print(f"  - Variable: {DISPLAY_COLOR}")
        if TESTING_MODE:
            print(f"  - Testing Mode: Rendered {TEST_CAMERA} view only")
        else:
            print(f"  - Rendered all sphere views")
    
    elif RENDER_OBJECT == "robinson":
        if 'robinson_filename' in locals() and robinson_filename:
            print(f"ROBINSON: {os.path.basename(robinson_filename)}")
        print(f"  - Variable: {DISPLAY_COLOR}")
        print(f"  - Camera: Top-view orthographic (perfect fit)")
        print(f"  - Resolution: {ROBINSON_SETTINGS['resolution_width']} x {ROBINSON_SETTINGS['resolution_width']//2}")
        print(f"  - Mesh: 4x subdivisions + simple subsurf")
    
    if WOW_MODE:
        print(f"WOW MODE: Enhanced visual effects active")
    
    if COLORBAR_OVERLAY:
        print(f"COLORBAR OVERLAY: Generated with overlays")
    
    print(f"\nOutput Location:")
    script_dir = os.path.dirname(bpy.data.filepath)
    data_sphere_dir = os.path.dirname(script_dir)
    if RENDER_OBJECT == "sphere":
        print(f"   {os.path.join(data_sphere_dir, 'Output', 'Sphere')}")
    elif RENDER_OBJECT == "robinson":
        print(f"   {os.path.join(data_sphere_dir, 'Output', 'Robinson')}")
    
    print("="*70)

# Run the script
if __name__ == "__main__":
    main()