import bpy
import os
import glob
import math
import sys

import matplotlib.pyplot as plt
import numpy as np

import argparse

CUSTOM_COLOR_RAMPS = {
    # Original climate data color schemes
    "precipitation": [
        (0.0, [0.0, 0.0, 0.0, 1.0]),
        (0.05263155698776245, [0.061205919831991196, 0.0037467454094439745, 0.13492080569267273, 1.0]),
        (0.10526317358016968, [0.06187712028622627, 0.01448772568255663, 0.18247292935848236, 1.0]),
        (0.15789473056793213, [0.05637719854712486, 0.03366807848215103, 0.22444787621498108, 1.0]),
        (0.21052634716033936, [0.0475434735417366, 0.058084726333618164, 0.25060197710990906, 1.0]),
        (0.2631579041481018, [0.0371728353202343, 0.09017402678728104, 0.26632359623908997, 1.0]),
        (0.31578946113586426, [0.028809722512960434, 0.12429725378751755, 0.2734186053276062, 1.0]),
        (0.3684210777282715, [0.021840587258338928, 0.16534572839736938, 0.27672967314720154, 1.0]),
        (0.42105263471603394, [0.016847146674990654, 0.20782506465911865, 0.2770037353038788, 1.0]),
        (0.4736841917037964, [0.012492450885474682, 0.25902366638183594, 0.2732461988925934, 1.0]),
        (0.5263158082962036, [0.009742427617311478, 0.3121352791786194, 0.2637326419353485, 1.0]),
        (0.5789473652839661, [0.010268782265484333, 0.3752182126045227, 0.24440304934978485, 1.0]),
        (0.6315789222717285, [0.018240107223391533, 0.43827247619628906, 0.21680444478988647, 1.0]),
        (0.6842105388641357, [0.04304962232708931, 0.5088575482368469, 0.17744702100753784, 1.0]),
        (0.7368420958518982, [0.09070251882076263, 0.5740482211112976, 0.13471432030200958, 1.0]),
        (0.7894737124443054, [0.18001516163349152, 0.639945924282074, 0.08708430826663971, 1.0]),
        (0.8421052694320679, [0.3082120418548584, 0.6933635473251343, 0.04732321947813034, 1.0]),
        (0.8947368264198303, [0.5017335414886475, 0.7396805882453918, 0.016790039837360382, 1.0]),
        (0.9473684430122375, [0.7287082672119141, 0.7735996842384338, 0.00576141057536006, 1.0]),
        (1.0, [0.9852057695388794, 0.8050958514213562, 0.014059592969715595, 1.0])
    ],
    
    "temperature": [
        (0.0, [0.0, 0.0, 0.0, 1.0]),
        (0.05263155698776245, [0.003496936522424221, 0.0, 0.0, 1.0]),
        (0.10526317358016968, [0.01606770046055317, 0.0, 0.0, 1.0]),
        (0.15789473056793213, [0.041451890021562576, 0.0, 0.0, 1.0]),
        (0.21052634716033936, [0.07698733359575272, 0.0, 0.0, 1.0]),
        (0.2631579041481018, [0.12893681228160858, 0.0, 0.0, 1.0]),
        (0.31578946113586426, [0.1904628723859787, 0.0, 0.0, 1.0]),
        (0.3684210777282715, [0.2715774178504944, 0.0, 0.0, 1.0]),
        (0.42105263471603394, [0.36112427711486816, 0.0, 0.0, 1.0]),
        (0.4736841917037964, [0.47330400347709656, 0.0, 0.0, 1.0]),
        (0.5263158082962036, [0.5924380421638489, 0.0014331345446407795, 0.0, 1.0]),
        (0.5789473652839661, [0.7372047901153564, 0.017936432734131813, 0.0, 1.0]),
        (0.6315789222717285, [0.8872158527374268, 0.05284162610769272, 0.0, 1.0]),
        (0.6842105388641357, [1.0, 0.11392093449831009, 0.0, 1.0]),
        (0.7368420958518982, [1.0, 0.1939721703529358, 0.0, 1.0]),
        (0.7894737124443054, [1.0, 0.3066347539424896, 0.019917838275432587, 1.0]),
        (0.8421052694320679, [1.0, 0.43681275844573975, 0.11392093449831009, 1.0]),
        (0.8947368264198303, [1.0, 0.6054843068122864, 0.3157627582550049, 1.0]),
        (0.9473684430122375, [1.0, 0.7893137335777283, 0.6054843068122864, 1.0]),
        (1.0, [1.0, 1.0, 1.0, 1.0])
    ],
    
    "precip_dif": [
        (0.0, [1.0, 1.0, 1.0, 1.0]),
        (0.055555541068315506, [1.0, 0.5795466303825378, 0.28012436628341675, 1.0]),
        (0.1111111119389534, [1.0, 0.28012436628341675, 0.00969632901251316, 1.0]),
        (0.1666666567325592, [1.0, 0.08919350802898407, 0.0, 1.0]),
        (0.2222222238779068, [0.6730490922927856, 0.008373118005692959, 0.0, 1.0]),
        (0.2777777910232544, [0.4071786105632782, 0.0, 0.0, 1.0]),
        (0.3333333432674408, [0.21763764321804047, 0.0, 0.0, 1.0]),
        (0.3888888955116272, [0.08690125495195389, 0.0, 0.0, 1.0]),
        (0.4444444477558136, [0.018912984058260918, 0.0, 0.0, 1.0]),
        (0.5, [0.0, 0.0, 0.0, 1.0]),
        (0.5555555820465088, [0.000493000028654933, 0.025371000170707703, 0.14799800515174866, 1.0]),
        (0.6111111640930176, [0.000493000028654933, 0.07173699885606766, 0.31137698888778687, 1.0]),
        (0.6666667461395264, [0.007108999881893396, 0.14263400435447693, 0.436381995677948, 1.0]),
        (0.7222223281860352, [0.03423000127077103, 0.2468000054359436, 0.5376899838447571, 1.0]),
        (0.777777910232544, [0.09710799902677536, 0.3649109899997711, 0.6301739811897278, 1.0]),
        (0.8333334922790527, [0.2279060035943985, 0.5038710236549377, 0.7154939770698547, 1.0]),
        (0.8888890743255615, [0.41693100333213806, 0.6365299820899963, 0.7943779826164246, 1.0]),
        (0.9444446563720703, [0.6109790205955505, 0.74372398853302, 0.8827369809150696, 1.0]),
        (1.0, [0.9322770237922668, 0.965815007686615, 1.0, 1.0])
    ],
    
    "temp_dif": [
        (0.0, [0.9322770237922668, 0.965815007686615, 1.0, 1.0]),
        (0.05555534362792969, [0.6109790205955505, 0.74372398853302, 0.8827369809150696, 1.0]),
        (0.11111092567443848, [0.41693100333213806, 0.6365299820899963, 0.7943779826164246, 1.0]),
        (0.16666650772094727, [0.2279060035943985, 0.5038710236549377, 0.7154939770698547, 1.0]),
        (0.22222208976745605, [0.09710799902677536, 0.3649109899997711, 0.6301739811897278, 1.0]),
        (0.27777767181396484, [0.03423000127077103, 0.2468000054359436, 0.5376899838447571, 1.0]),
        (0.33333325386047363, [0.007108999881893396, 0.14263400435447693, 0.436381995677948, 1.0]),
        (0.3888888359069824, [0.000493000028654933, 0.07173699885606766, 0.31137698888778687, 1.0]),
        (0.4444444179534912, [0.000493000028654933, 0.025371000170707703, 0.14799800515174866, 1.0]),
        (0.5, [0.0, 0.0, 0.0, 1.0]),
        (0.5555555820465088, [0.018912984058260918, 0.0, 0.0, 1.0]),
        (0.6111111044883728, [0.08690125495195389, 0.0, 0.0, 1.0]),
        (0.6666666269302368, [0.21763764321804047, 0.0, 0.0, 1.0]),
        (0.7222222089767456, [0.4071786105632782, 0.0, 0.0, 1.0]),
        (0.7777777910232544, [0.6730490922927856, 0.008373118005692959, 0.0, 1.0]),
        (0.8333333730697632, [1.0, 0.08919350802898407, 0.0, 1.0]),
        (0.8888888955116272, [1.0, 0.28012436628341675, 0.00969632901251316, 1.0]),
        (0.944444477558136, [1.0, 0.5795466303825378, 0.28012436628341675, 1.0]),
        (1.0, [1.0, 1.0, 1.0, 1.0])
    ],

    # ==============================================================================
    # CUSTOM USER COLOR SCHEMES
    # ==============================================================================
    
    # Example custom precipitation scheme
    "jw_precip": [
        (0.0, [0.05, 0.05, 0.2, 1.0]),      # Dark blue (dry)
        (0.25, [0.2, 0.4, 0.8, 1.0]),       # Medium blue
        (0.5, [0.4, 0.8, 0.4, 1.0]),        # Green (moderate)
        (0.75, [0.9, 0.9, 0.2, 1.0]),       # Yellow (wet)
        (1.0, [0.9, 0.2, 0.1, 1.0])         # Red (very wet)
    ],
    
    # Example custom temperature scheme  
    "jw_temp": [
        (0.0, [0.1, 0.1, 0.5, 1.0]),        # Deep blue (cold)
        (0.2, [0.3, 0.3, 0.9, 1.0]),        # Light blue
        (0.4, [0.9, 0.9, 0.9, 1.0]),        # White (neutral)
        (0.6, [0.9, 0.7, 0.3, 1.0]),        # Orange
        (0.8, [0.9, 0.3, 0.1, 1.0]),        # Red
        (1.0, [0.6, 0.1, 0.1, 1.0])         # Dark red (hot)
    ],
    
    # Ocean depth inspired scheme
    "ocean_depth": [
        (0.0, [0.0, 0.1, 0.2, 1.0]),        # Deep ocean
        (0.3, [0.0, 0.3, 0.5, 1.0]),        # Mid ocean
        (0.6, [0.2, 0.6, 0.8, 1.0]),        # Shallow water
        (0.8, [0.6, 0.9, 0.9, 1.0]),        # Very shallow
        (1.0, [0.9, 0.95, 1.0, 1.0])        # Surface
    ],
    
    # Earth tones scheme
    "earth_tones": [
        (0.0, [0.2, 0.1, 0.0, 1.0]),        # Dark brown
        (0.25, [0.5, 0.3, 0.1, 1.0]),       # Brown
        (0.5, [0.7, 0.6, 0.3, 1.0]),        # Tan
        (0.75, [0.4, 0.6, 0.2, 1.0]),       # Olive green
        (1.0, [0.2, 0.4, 0.1, 1.0])         # Forest green
    ],
    
    # Fire scheme
    "fire": [
        (0.0, [0.0, 0.0, 0.0, 1.0]),        # Black
        (0.25, [0.3, 0.0, 0.1, 1.0]),       # Dark red
        (0.5, [0.8, 0.2, 0.0, 1.0]),        # Red
        (0.75, [1.0, 0.6, 0.1, 1.0]),       # Orange
        (1.0, [1.0, 1.0, 0.8, 1.0])         # White-yellow
    ]
}

# ==============================================================================
# POPULAR MATPLOTLIB COLORMAPS
# ==============================================================================

# List of popular matplotlib colormaps that work well for scientific data
# These will be dynamically loaded from matplotlib when requested

MATPLOTLIB_COLORMAPS = [
    # Sequential (single hue)
    'viridis', 'plasma', 'inferno', 'magma', 'cividis',
    
    # Sequential (multi-hue)
    'Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Greys', 'Oranges', 
    'OrRd', 'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu', 'Reds', 
    'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd',
    
    # Diverging (good for difference data)
    'coolwarm', 'bwr', 'seismic', 'RdBu', 'RdGy', 'RdYlBu', 
    'RdYlGn', 'Spectral', 'BrBG', 'PiYG', 'PRGn', 'PuOr',
    
    # Cyclic
    'twilight', 'twilight_shifted', 'hsv',
    
    # Miscellaneous
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'gist_rainbow',
    'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'
]

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def is_matplotlib_colormap(colormap_name):
    """Check if colormap name is a matplotlib colormap"""
    return colormap_name in MATPLOTLIB_COLORMAPS

def is_custom_colormap(colormap_name):
    """Check if colormap name is a custom colormap"""
    return colormap_name in CUSTOM_COLOR_RAMPS

def get_custom_colormap(colormap_name):
    """Get custom colormap data"""
    if colormap_name in CUSTOM_COLOR_RAMPS:
        return CUSTOM_COLOR_RAMPS[colormap_name]
    else:
        raise ValueError(f"Custom colormap '{colormap_name}' not found")

        
parser = argparse.ArgumentParser()
parser.add_argument("input_tiff")
parser.add_argument("output_dir")
parser.add_argument("--resource")
parser.add_argument("--locations", default="Europe", help="comma separated list of locations to plot")

parser.add_argument("--variable", default="temperature", choices=['2t', 'precipitation', 'precip_dif', 'temp_dif'])
parser.add_argument("--vmin", default=0, type=float)
parser.add_argument("--vmax", default=10, type=float)

parser.add_argument("--do-overlay", action="store_true")
parser.add_argument("--overlay-color", default="black")
parser.add_argument("--overlay-opacity", default=0, type=float)


parser.add_argument("--zoomlevel", default=0)
parser.add_argument("--dof", action="store_true")

parser.add_argument("--effects", action="store_true", help="add some special effect, like glow")
parser.add_argument("--lowres", action="store_true")

if "--" in sys.argv:
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
else:
    args = parser.parse_args()

# parse location string into list
args.locations = [s.strip() for s in args.locations.split(",")]

# B) Color Selection - Choose from individual or common libraries
DISPLAY_COLOR = args.variable 

# C) Map Range Settings
MAP_RANGE = {
    "from_min": args.vmin,      # Minimum value in your data
    "from_max": args.vmax,      # Maximum value in your data
    "to_min": 0.0,      # Maps to color ramp start
    "to_max": 1.0       # Maps to color ramp end
}

# D) Overlay
COLORBAR_OVERLAY = args.do_overlay  # Create composite images with colorbars
OVERLAY_SETTINGS = {
    "position": "top_right",        # Colorbar position
    "colorbar_text": args.overlay_color,       # Text color
    "colorbar_scale": 0.4,          # Scale relative to image height
    "colorbar_steps": 6,            # Number of tick marks
    "padding": 50,                  # Padding from edges
    "background_opacity": args.overlay_opacity       # Background transparency
}

# E) Plot Type and Styling
WOW_MODE = args.effects  # Glossy surface, emission glow, displacement, adds "_wow" to filenames
RENDER_OBJECT = "sphere"  # Options: "sphere" or "robinson"

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
    "zoom_level": args.zoomlevel, # 0 = full sphere visible, 0.5 = close zoom
    "distance": 6,                # Distance from sphere center
    "depth_of_field": args.dof,       # Enable/disable depth of field effect
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
    "Marrakech_Atlas": (31.6, -8.0),
    "Congo_River": (0, 18),
    "Himalayas": (28, 87),               
    "Bremen": (53.08, 8.80)
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


def srgb_to_linear(srgb_value):
    """Convert sRGB color value to linear RGB"""
    if srgb_value <= 0.04045:
        return srgb_value / 12.92
    else:
        return pow((srgb_value + 0.055) / 1.055, 2.4)

def matplotlib_to_blender_colormap(colormap_name, num_samples=20):
    """Convert a matplotlib colormap to Blender color ramp format with proper color space conversion"""
    
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
        

def get_colormap_data(colormap_name):
    """Get colormap data for the specified colormap name"""
    
    # Check if it's a custom colormap
    if is_custom_colormap(colormap_name):
        print(f"Using custom colormap: {colormap_name}")
        return get_custom_colormap(colormap_name)
    
    # Check if it's a matplotlib colormap
    elif is_matplotlib_colormap(colormap_name):
        print(f"Using matplotlib colormap: {colormap_name}")
        return matplotlib_to_blender_colormap(colormap_name, num_samples=20)
            


# ==============================================================================
# MAIN SCRIPT FUNCTIONS
# ==============================================================================

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)


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

def setup_color_ramp(color_ramp_node, colormap_name):
    
    # Get the colormap data
    colors = get_colormap_data(colormap_name)
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

def create_climate_material(obj, geotiff_path, is_robinson=False):
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
    geotiff_path = os.path.abspath(geotiff_path)
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
    setup_color_ramp(color_ramp, DISPLAY_COLOR)
    
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
    selected_positions = {key: all_positions[key] for key in args.locations}

    print(f"Creating {len(all_positions)} sphere cameras (focal length: {adjusted_focal}mm)")
    if use_dof or WOW_MODE:
        sphere_radius = 2.0
        focus_dist = distance - sphere_radius
        print(f"  DOF enabled (f/{aperture_fstop}, focus at sphere surface: {focus_dist} units)")
    
    for location_name, (lat, lon) in selected_positions.items():
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

def setup_render_settings(obj_type="sphere", lowres=False):
    """Configure render settings for sphere or Robinson"""
    scene = bpy.context.scene
    
    if obj_type == "robinson":
        # 4:2 aspect ratio for Robinson
        scene.render.resolution_x = ROBINSON_SETTINGS["resolution_width"]
        scene.render.resolution_y = ROBINSON_SETTINGS["resolution_width"] // 2
        print(f"Robinson render settings: {scene.render.resolution_x} x {scene.render.resolution_y}")
    else:
        # Square for sphere
        if lowres:
            scene.render.resolution_x = 200
            scene.render.resolution_y = 200
        else:
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
    if lowres:
        scene.cycles.samples = 32
    
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

def generate_scientific_colorbars(output_dir, variable_type, from_min, from_max, suffix="" ):
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
        if is_matplotlib_colormap(variable_type):
            # Use matplotlib colormap directly
            cmap = plt.get_cmap(variable_type)
            print(f"Using matplotlib colormap directly: {variable_type}")
        else:
            # Create from custom colormap data
            colors_data = get_colormap_data(variable_type)
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
    
    if obj_type == "sphere":
        # All continent and interest positions
        all_positions = {**CONTINENT_POSITIONS, **INTEREST_POSITIONS}
        selected_positions = {key: all_positions[key] for key in args.locations if key in all_positions}
        for location_name in selected_positions.keys():
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

def render_object_cameras(cameras, input_filename, output_dir, obj_type="sphere"):
    """Render views from cameras"""
    data_sphere_dir = os.path.dirname(output_dir)
    
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
        )
        create_overlays_for_renders(output_dir, input_filename, suffix, obj_type)

def main():
    print("CLIMATE GLOBE GENERATOR")
    
    # 1. Clear scene
    print("1. Clearing scene...")
    clear_scene()
    
    # 2. Add lighting
    print("2. Adding lighting...")
    add_lighting()
    
    # 3. Create object based on selection
    if RENDER_OBJECT == "sphere":
        print("3. Creating SPHERE...")
        
        geotiff_path = args.input_tiff
        input_filename = filename = os.path.splitext(os.path.basename(geotiff_path))[0]
        
        sphere = create_sphere()
        sphere_material = create_climate_material(sphere, geotiff_path, is_robinson=False)
        cameras = create_continent_cameras()
        
        print(f"Sphere setup complete ({len(cameras)} cameras)")
        
        # 4. Setup render settings and render
        print("4. Rendering SPHERE...")
        setup_render_settings("sphere", args.lowres)
        render_object_cameras(cameras, input_filename, args.output_dir, "sphere")
        bpy.ops.wm.save_as_mainfile(filepath="./blendertest.blend")
        
    elif RENDER_OBJECT == "robinson":
        print("3. Creating ROBINSON...")
        
        robinson_geotiff_path = args.input_tiff
        robinson_filename = os.path.splitext(os.path.basename(geotiff_path))[0]
        if not robinson_geotiff_path:
            print("Warning: No Robinson GeoTIFF found, continuing with procedural colors only")
        
        robinson = create_robinson_plane()
        robinson_material = create_climate_material(robinson, robinson_geotiff_path, is_robinson=True)
        cameras = create_robinson_camera()
        
        print(f"Robinson setup complete (1 camera)")
        
        # 4. Setup render settings and render
        print("4. Rendering ROBINSON...")
        setup_render_settings("robinson")
        render_object_cameras(cameras, robinson_filename, args.output_dir, "robinson")
    
    else:
        print(f"ERROR: Invalid RENDER_OBJECT '{RENDER_OBJECT}'. Use 'sphere' or 'robinson'")
        return
    

# Run the script
if __name__ == "__main__":
    main()
