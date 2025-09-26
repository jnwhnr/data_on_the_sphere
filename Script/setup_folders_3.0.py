#!/usr/bin/env python3
"""
Climate Globe Generator - Enhanced Folder Structure Setup with Robinson Projection
Creates the required folder structure and handles map reprojection for both sphere and Robinson outputs.
Run this script first before using the main Blender script.
"""

import os
import subprocess
import glob
import shutil

def create_folder_structure():
    """Create the required folder structure for Climate Globe Generator with projection support"""
    
    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go up one level to create the main project structure
    project_root = os.path.dirname(script_dir)
    
    # Define enhanced folder structure with projection folders
    folders_to_create = [
        os.path.join(project_root, "Input"),
        os.path.join(project_root, "Input", "EPSG:4326"),      # Plate Carrée (sphere input)
        os.path.join(project_root, "Input", "ESRI:54030"),     # Robinson projection (plane input)
        os.path.join(project_root, "Output"),
        os.path.join(project_root, "Output", "Sphere"),
        os.path.join(project_root, "Output", "Robinson")
    ]
    
    print("Climate Globe Generator - Enhanced Folder Structure Setup")
    print("=" * 60)
    print(f"Project root: {project_root}")
    print()
    
    created_folders = []
    existing_folders = []
    
    # Create folders
    for folder_path in folders_to_create:
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
                created_folders.append(os.path.relpath(folder_path, project_root))
            else:
                existing_folders.append(os.path.relpath(folder_path, project_root))
        except OSError as e:
            print(f"Error creating folder {folder_path}: {e}")
            return False
    
    # Report folder creation results
    if created_folders:
        print("Created folders:")
        for folder in created_folders:
            print(f"  ✅ {folder}/")
    
    if existing_folders:
        print("Already existing:")
        for folder in existing_folders:
            print(f"  - {folder}/")
    
    print()
    
    # Handle map reprojection
    handle_map_reprojection(project_root)
    
    print()
    print("Folder structure ready!")
    print()
    print("Folder structure:")
    print("  Input/")
    print("    ├── EPSG:4326/     (Plate Carrée maps for sphere)")
    print("    └── ESRI:54030/    (Robinson projection maps for plane)")
    print("  Output/")
    print("    ├── Sphere/        (Sphere renderings)")
    print("    └── Robinson/      (Robinson plane renderings)")
    print()
    print("Next steps:")
    print("1. Configure object selection in the main Blender script")
    print("2. Run the main Blender script")
    print("3. Find rendered images in Output/Sphere/ and Output/Robinson/")
    
    return True

def check_gdal_installation():
    """Check if GDAL is installed and accessible"""
    print("🔍 Checking GDAL installation...")
    try:
        result = subprocess.run(['gdalwarp', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_info = result.stdout.strip().split('\n')[0]
            print(f"  ✅ GDAL found: {version_info}")
            return True
        else:
            print(f"  ❌ GDAL command failed with return code: {result.returncode}")
            print(f"  Error output: {result.stderr}")
            return False
    except FileNotFoundError:
        print("  ⚠️  GDAL not found in system PATH")
        print("     Install GDAL to enable automatic Robinson reprojection")
        print("     - Windows: Download from https://gdal.org/download.html")
        print("     - macOS: brew install gdal")
        print("     - Ubuntu/Debian: sudo apt-get install gdal-bin")
        print("     - Check if GDAL is in your PATH environment variable")
        return False
    except subprocess.TimeoutExpired:
        print("  ⚠️  GDAL command timed out")
        return False
    except Exception as e:
        print(f"  ⚠️  Error checking GDAL: {e}")
        return False

def reproject_to_robinson(input_path, output_path):
    """Use gdalwarp to reproject Plate Carrée to Robinson projection"""
    try:
        # Verify input file exists and is readable
        if not os.path.exists(input_path):
            print(f"    ❌ Input file not found: {input_path}")
            return False
            
        file_size = os.path.getsize(input_path)
        print(f"    📁 Input file: {os.path.basename(input_path)} ({file_size:,} bytes)")
        
        # Use corrected command with -9999 nodata value
        cmd = [
            "gdalwarp",
            "-s_srs", "EPSG:4326",
            "-t_srs", "ESRI:54030",
            "-te", "-17000000", "-8500000", "17000000", "8500000",
            "-ts", "5000", "2500", 
            "-r", "bilinear",
            "-dstnodata", "-9999",     # Use -9999 instead of 255 to avoid edge artifacts
            "-of", "GTiff",
            input_path,
            output_path
        ]
        
        print(f"    🔄 Reprojecting: {os.path.basename(input_path)} → {os.path.basename(output_path)}")
        print(f"    📋 Command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # Check if output file was created and has reasonable size
            if os.path.exists(output_path):
                output_size = os.path.getsize(output_path)
                print(f"    ✅ Success! Output file: {output_size:,} bytes")
                return True
            else:
                print(f"    ❌ Command succeeded but output file not found!")
                return False
        else:
            print(f"    ❌ GDAL command failed (return code: {result.returncode})")
            if result.stderr:
                print(f"    📄 Error details: {result.stderr.strip()}")
            if result.stdout:
                print(f"    📄 Output: {result.stdout.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"    ⚠️  Reprojection timed out (>5 minutes)")
        return False
    except Exception as e:
        print(f"    ❌ Reprojection error: {e}")
        import traceback
        print(f"    📋 Full error: {traceback.format_exc()}")
        return False

def handle_map_reprojection(project_root):
    """Move plate carrée maps and create Robinson projections"""
    
    print("Checking for maps and handling reprojection...")
    
    # Check if GDAL is available
    gdal_available = check_gdal_installation()
    print()
    
    # Find TIFF files in main Input folder
    input_folder = os.path.join(project_root, "Input")
    tiff_files = []
    
    # Look for various TIFF extensions
    for pattern in ["*.tif", "*.tiff", "*.TIF", "*.TIFF"]:
        tiff_files.extend(glob.glob(os.path.join(input_folder, pattern)))
    
    if not tiff_files:
        print("No TIFF files found in Input/ folder")
        print("Place your Plate Carrée GeoTIFF files in Input/ and run this script again")
        return
    
    epsg4326_folder = os.path.join(input_folder, "EPSG:4326")
    esri54030_folder = os.path.join(input_folder, "ESRI:54030")
    
    moved_files = 0
    reprojected_files = 0
    
    print(f"Found {len(tiff_files)} TIFF file(s) to process:")
    
    for tiff_file in tiff_files:
        filename = os.path.basename(tiff_file)
        base_name = os.path.splitext(filename)[0]
        
        print(f"\n  Processing: {filename}")
        
        # Move original to EPSG:4326 folder
        epsg_path = os.path.join(epsg4326_folder, filename)
        try:
            if not os.path.exists(epsg_path):
                shutil.move(tiff_file, epsg_path)
                print(f"    ✅ Moved to EPSG:4326/")
                moved_files += 1
            else:
                print(f"    - Already exists in EPSG:4326/")
                # Remove the original if it exists in main folder
                if os.path.exists(tiff_file):
                    os.remove(tiff_file)
        except Exception as e:
            print(f"    ❌ Failed to move: {e}")
            continue
        
        # Create Robinson projection if GDAL is available
        if gdal_available:
            robinson_filename = f"{base_name}_robinson.tif"
            robinson_path = os.path.join(esri54030_folder, robinson_filename)
            
            if not os.path.exists(robinson_path):
                if reproject_to_robinson(epsg_path, robinson_path):
                    print(f"    ✅ Created Robinson projection: {robinson_filename}")
                    reprojected_files += 1
                else:
                    print(f"    ❌ Failed to create Robinson projection")
            else:
                print(f"    - Robinson projection already exists")
        else:
            print(f"    ⚠️  Skipping Robinson reprojection (GDAL not available)")
    
    # Summary
    print(f"\n📊 Processing Summary:")
    print(f"  - Files moved to EPSG:4326/: {moved_files}")
    if gdal_available:
        print(f"  - Robinson projections created: {reprojected_files}")
    else:
        print(f"  - Robinson projections skipped: {len(tiff_files)} (install GDAL to enable)")
    
    # Create Robinson mask automatically
    print(f"\n🎭 Robinson Mask Generation:")
    if create_automatic_robinson_mask(esri54030_folder, epsg4326_folder):
        print(f"  ✅ Robinson mask created successfully")
    else:
        print(f"  ⚠️  Automatic mask creation failed - manual creation needed")
    
    if not gdal_available and tiff_files:
        print(f"\n💡 To enable Robinson projection:")
        print(f"   1. Install GDAL on your system")
        print(f"   2. Run this script again")
        print(f"   3. Robinson projections will be created automatically")

def create_robinson_mask_from_data(input_path, mask_path):
    """Create Robinson mask from actual reprojected data using GDAL"""
    try:
        print(f"    🎭 Creating Robinson mask from data: {os.path.basename(input_path)}")
        
        # Step 1: Create temporary Robinson projection of the input data
        temp_robinson = mask_path.replace('.tif', '_temp_data.tif')
        
        cmd_reproject = [
            "gdalwarp",
            "-s_srs", "EPSG:4326",        # Source: Plate Carrée
            "-t_srs", "ESRI:54030",       # Target: Robinson projection  
            "-te", "-17000000", "-8500000", "17000000", "8500000",  # Target extent
            "-ts", "5000", "2500",        # Target size (4:2 aspect ratio)
            "-r", "bilinear",             # Resampling method
            "-dstnodata", "-9999",        # Use -9999 instead of 255
            "-of", "GTiff",               # Output format
            input_path,
            temp_robinson
        ]
        
        print(f"    📊 Reprojecting for mask creation...")
        result = subprocess.run(cmd_reproject, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print(f"    ❌ Mask reprojection failed: {result.stderr}")
            return False
        
        if not os.path.exists(temp_robinson):
            print(f"    ❌ Temporary Robinson file not created")
            return False
        
        # Step 2: Create mask using gdal_calc.py - valid data = 255, nodata = 0
        cmd_mask = [
            "gdal_calc.py",
            "-A", temp_robinson,
            f"--outfile={mask_path}",
            "--calc=(A!=-9999)*255",      # If A is not nodata (-9999), set to 255 (white), else 0 (black)
            "--type=Byte",
            "--NoDataValue=0"
        ]
        
        print(f"    🖼️  Creating mask from reprojected data...")
        mask_result = subprocess.run(cmd_mask, capture_output=True, text=True, timeout=120)
        
        # Clean up temporary file
        if os.path.exists(temp_robinson):
            os.remove(temp_robinson)
        
        if mask_result.returncode == 0 and os.path.exists(mask_path):
            file_size = os.path.getsize(mask_path)
            print(f"    ✅ Robinson mask created from data: {file_size:,} bytes")
            return True
        else:
            print(f"    ❌ Mask creation failed: {mask_result.stderr}")
            return False
            
    except FileNotFoundError as e:
        print(f"    ❌ GDAL tool not found: {e}")
        print(f"    💡 Make sure gdal_calc.py is in your PATH")
        return False
    except Exception as e:
        print(f"    ❌ Mask creation error: {e}")
        return False

def create_robinson_mask_alternative(input_path, mask_path):
    """Alternative Robinson mask creation using gdalwarp only"""
    try:
        print(f"    🎭 Creating Robinson mask (alternative method)...")
        
        # Create the mask directly by reprojecting and using the alpha band
        cmd_mask = [
            "gdalwarp",
            "-s_srs", "EPSG:4326",
            "-t_srs", "ESRI:54030", 
            "-te", "-17000000", "-8500000", "17000000", "8500000",
            "-ts", "5000", "2500",
            "-r", "near",                 # Nearest neighbor for mask
            "-dstnodata", "0",            # Nodata = 0 (black) for mask
            "-dstalpha",                  # Create alpha band
            "-of", "GTiff",
            input_path,
            mask_path
        ]
        
        result = subprocess.run(cmd_mask, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and os.path.exists(mask_path):
            # Convert to single band mask (extract alpha channel)
            temp_mask = mask_path.replace('.tif', '_temp_mask.tif')
            
            cmd_extract = [
                "gdal_translate",
                "-b", "2",                # Extract band 2 (alpha)
                "-ot", "Byte",
                mask_path,
                temp_mask
            ]
            
            extract_result = subprocess.run(cmd_extract, capture_output=True, text=True, timeout=60)
            
            if extract_result.returncode == 0:
                # Replace original with single-band mask
                os.replace(temp_mask, mask_path)
                file_size = os.path.getsize(mask_path)
                print(f"    ✅ Alternative Robinson mask created: {file_size:,} bytes")
                return True
        
        print(f"    ❌ Alternative mask creation failed")
        return False
        
    except Exception as e:
        print(f"    ❌ Alternative mask creation error: {e}")
        return False

def create_robinson_mask_simple_gdal(input_path, mask_path):
    """Simple GDAL-only mask creation"""
    try:
        print(f"    🎭 Creating simple GDAL mask...")
        
        # Reproject with specific nodata handling to create binary mask
        cmd = [
            "gdalwarp",
            "-s_srs", "EPSG:4326",
            "-t_srs", "ESRI:54030",
            "-te", "-17000000", "-8500000", "17000000", "8500000", 
            "-ts", "5000", "2500",
            "-r", "near",
            "-srcnodata", "None",         # Treat no pixels as nodata in source
            "-dstnodata", "0",            # Set output nodata to 0 (black) for mask
            "-ot", "Byte",                # Output as byte
            "-of", "GTiff",
            input_path,
            mask_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and os.path.exists(mask_path):
            # Post-process to create proper black/white mask
            temp_processed = mask_path.replace('.tif', '_processed.tif')
            
            # Use gdal_calc if available, otherwise keep as-is
            try:
                cmd_process = [
                    "gdal_calc.py",
                    "-A", mask_path,
                    f"--outfile={temp_processed}",
                    "--calc=(A>0)*255",       # Convert any data value to 255 (white)
                    "--type=Byte",
                    "--NoDataValue=0"
                ]
                
                proc_result = subprocess.run(cmd_process, capture_output=True, text=True, timeout=60)
                
                if proc_result.returncode == 0:
                    os.replace(temp_processed, mask_path)
                    
            except FileNotFoundError:
                # gdal_calc not available, keep original
                pass
            
            file_size = os.path.getsize(mask_path)
            print(f"    ✅ Simple GDAL mask created: {file_size:,} bytes")
            return True
        
        return False
        
    except Exception as e:
        print(f"    ❌ Simple GDAL mask error: {e}")
        return False

def create_automatic_robinson_mask(esri_folder, epsg_folder=None):
    """Create Robinson projection mask from actual data"""
    mask_path = os.path.join(esri_folder, "robinson_mask.tif")
    
    if os.path.exists(mask_path):
        print(f"  📋 Robinson mask already exists: robinson_mask.tif")
        return True
    
    # Find a source file to create the mask from
    source_files = []
    if epsg_folder and os.path.exists(epsg_folder):
        for pattern in ["*.tif", "*.tiff", "*.TIF", "*.TIFF"]:
            source_files.extend(glob.glob(os.path.join(epsg_folder, pattern)))
    
    # If no epsg_folder provided or no files found there, look in esri folder
    if not source_files:
        for pattern in ["*.tif", "*.tiff", "*.TIF", "*.TIFF"]:
            found_files = glob.glob(os.path.join(esri_folder, pattern))
            # Exclude mask files
            source_files.extend([f for f in found_files if 'mask' not in os.path.basename(f).lower()])
    
    if not source_files:
        print(f"  ⚠️  No source files found for mask creation")
        print(f"     Looked in: {epsg_folder if epsg_folder else esri_folder}")
        return False
    
    # Use the first available source file
    source_file = source_files[0]
    print(f"  🎭 Creating Robinson mask from: {os.path.basename(source_file)}")
    
    # Try different methods for mask creation
    methods = [
        ("Data-based mask (gdal_calc)", lambda: create_robinson_mask_from_data(source_file, mask_path)),
        ("Alternative method (alpha)", lambda: create_robinson_mask_alternative(source_file, mask_path)),
        ("Simple GDAL method", lambda: create_robinson_mask_simple_gdal(source_file, mask_path))
    ]
    
    for method_name, method_func in methods:
        print(f"    Trying: {method_name}")
        try:
            if method_func():
                return True
        except Exception as e:
            print(f"    ❌ {method_name} failed: {e}")
            continue
    
    print(f"    ⚠️  All mask creation methods failed")
    print(f"    💡 You can create robinson_mask.tif manually using:")
    print(f"       gdalwarp -s_srs EPSG:4326 -t_srs ESRI:54030 \\")
    print(f"                -te -17000000 -8500000 17000000 8500000 \\") 
    print(f"                -ts 5000 2500 -dstnodata -9999 -dstalpha \\")
    print(f"                {os.path.basename(source_file)} robinson_mask.tif")
    
    return False

def test_reprojection_comparison():
    """Test function to compare script output vs manual command"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    print("\n🧪 REPROJECTION COMPARISON TEST")
    print("=" * 40)
    
    # Find test file
    epsg_folder = os.path.join(project_root, "Input", "EPSG:4326")
    if not os.path.exists(epsg_folder):
        print("❌ EPSG:4326 folder not found")
        return False
    
    tiff_files = []
    for pattern in ["*.tif", "*.tiff", "*.TIF", "*.TIFF"]:
        tiff_files.extend(glob.glob(os.path.join(epsg_folder, pattern)))
    
    if not tiff_files:
        print("❌ No test files found in EPSG:4326 folder")
        return False
    
    test_input = tiff_files[0]
    base_name = os.path.splitext(os.path.basename(test_input))[0]
    
    esri_folder = os.path.join(project_root, "Input", "ESRI:54030")
    script_output = os.path.join(esri_folder, f"{base_name}_script_test.tif")
    manual_output = os.path.join(esri_folder, f"{base_name}_manual_test.tif")
    
    print(f"📁 Test input: {os.path.basename(test_input)}")
    print(f"📄 Script output: {os.path.basename(script_output)}")
    print(f"📄 Manual output: {os.path.basename(manual_output)}")
    
    # Test our script version
    print(f"\n🔄 Testing SCRIPT reprojection...")
    if reproject_to_robinson(test_input, script_output):
        script_size = os.path.getsize(script_output)
        print(f"✅ Script version created: {script_size:,} bytes")
    else:
        print(f"❌ Script version failed")
        return False
    
    # Show manual command for comparison
    print(f"\n📋 MANUAL COMMAND for comparison:")
    print(f"gdalwarp -s_srs EPSG:4326 -t_srs ESRI:54030 \\")
    print(f"         -te -17000000 -8500000 17000000 8500000 \\")
    print(f"         -ts 5000 2500 -r bilinear \\")
    print(f"         -dstnodata -9999 -of GTiff \\")
    print(f"         '{test_input}' \\")
    print(f"         '{manual_output}'")
    
    print(f"\n💡 Run the manual command above, then compare:")
    print(f"   Script:  {script_output}")
    print(f"   Manual:  {manual_output}")
    print(f"\n🔍 Use gdalinfo or a GIS viewer to compare the files")
    
    return True

def debug_gdalwarp_environment():
    """Debug GDAL environment and version"""
    print("\n🔍 GDAL ENVIRONMENT DEBUG")
    print("=" * 30)
    
    try:
        # Check GDAL version
        result = subprocess.run(['gdalwarp', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ GDAL Version: {result.stdout.strip()}")
        
        # Check available formats
        result = subprocess.run(['gdalwarp', '--formats'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            formats = [line for line in result.stdout.split('\n') if 'GTiff' in line]
            if formats:
                print(f"✅ GTiff Support: {formats[0].strip()}")
        
        # Check coordinate system support
        result = subprocess.run(['gdalsrsinfo', 'ESRI:54030'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Robinson Projection (ESRI:54030): Supported")
        else:
            print(f"⚠️  Robinson Projection support: {result.stderr.strip()}")
            
    except Exception as e:
        print(f"❌ GDAL environment check failed: {e}")
        
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            # Manual testing mode
            test_reprojection_comparison()
        elif sys.argv[1] == "--debug":
            # Debug GDAL environment
            debug_gdalwarp_environment()
        elif sys.argv[1] == "--compare":
            # Comparison testing mode
            test_reprojection_comparison()
        else:
            print("Usage:")
            print("  python setup_folders_robinson.py           # Normal setup")
            print("  python setup_folders_robinson.py --test    # Test reprojection")
            print("  python setup_folders_robinson.py --debug   # Debug GDAL environment")
            print("  python setup_folders_robinson.py --compare # Compare script vs manual")
    else:
        # Normal setup mode
        if create_folder_structure():
            print("\n🎯 Setup complete! Ready for Climate Globe Generator.")
            
            # Offer manual test if reprojection seemed to fail
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            esri_folder = os.path.join(project_root, "Input", "ESRI:54030")
            
            # Check if any .tif files were created (not just the txt file)
            tiff_files = []
            if os.path.exists(esri_folder):
                for pattern in ["*.tif", "*.tiff", "*.TIF", "*.TIFF"]:
                    found_files = glob.glob(os.path.join(esri_folder, pattern))
                    # Exclude mask files from count
                    tiff_files.extend([f for f in found_files if 'mask' not in os.path.basename(f).lower()])
            
            if not tiff_files:
                print("\n🔧 No Robinson projections found.")
                print("   For debugging:")
                print("   python setup_folders_robinson.py --debug   # Check GDAL")
                print("   python setup_folders_robinson.py --compare # Test reprojection")