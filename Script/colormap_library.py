    # ==============================================================================
# CLIMATE GLOBE GENERATOR - COLOR LIBRARY
# External colormap definitions for flexible color selection
# ==============================================================================

"""
Climate Globe Generator - Colormap Library

This file contains custom colormap definitions that can be used alongside
matplotlib's standard colormaps. 

Usage:
- Custom maps: Use names like "jw_precip", "climate_temp", etc.
- Matplotlib maps: Use standard names like "plasma", "viridis", "coolwarm", etc.
- Original maps: "precipitation", "temperature", "precip_dif", "temp_dif"
"""

# ==============================================================================
# CUSTOM COLOR RAMPS (Blender format: position, [R, G, B, A])
# ==============================================================================

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

def get_available_colormaps():
    """Get list of all available colormaps (custom + matplotlib)"""
    custom_maps = list(CUSTOM_COLOR_RAMPS.keys())
    return {
        'custom': custom_maps,
        'matplotlib': MATPLOTLIB_COLORMAPS,
        'all': custom_maps + MATPLOTLIB_COLORMAPS
    }

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

def matplotlib_to_blender_colormap(colormap_name, num_samples=20):
    """
    Convert a matplotlib colormap to Blender color ramp format
    
    Args:
        colormap_name: Name of matplotlib colormap
        num_samples: Number of color samples to take from the colormap
        
    Returns:
        List of (position, [R, G, B, A]) tuples for Blender
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Get the colormap
        cmap = plt.get_cmap(colormap_name)
        
        # Sample colors
        positions = np.linspace(0, 1, num_samples)
        colors = []
        
        for pos in positions:
            rgba = cmap(pos)
            colors.append((pos, [rgba[0], rgba[1], rgba[2], rgba[3]]))
        
        return colors
        
    except ImportError:
        print(f"Warning: matplotlib not available, cannot load colormap '{colormap_name}'")
        # Fallback to a simple gradient
        return [
            (0.0, [0.0, 0.0, 0.0, 1.0]),
            (1.0, [1.0, 1.0, 1.0, 1.0])
        ]
    except Exception as e:
        print(f"Error loading matplotlib colormap '{colormap_name}': {e}")
        return [
            (0.0, [0.0, 0.0, 0.0, 1.0]),
            (1.0, [1.0, 1.0, 1.0, 1.0])
        ]

def print_available_colormaps():
    """Print all available colormaps organized by category"""
    maps = get_available_colormaps()
    
    print("\n" + "="*60)
    print("AVAILABLE COLORMAPS")
    print("="*60)
    
    print(f"\nCUSTOM COLORMAPS ({len(maps['custom'])})")
    print("-" * 30)
    for i, name in enumerate(maps['custom'], 1):
        print(f"  {i:2d}. {name}")
    
    print(f"\nMATTPLOTLIB COLORMAPS ({len(maps['matplotlib'])})")
    print("-" * 30)
    
    # Group matplotlib maps by type
    sequential_single = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
    diverging = ['coolwarm', 'bwr', 'seismic', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral']
    
    print("  Popular Sequential:")
    for name in sequential_single:
        print(f"    • {name}")
    
    print("  Popular Diverging:")
    for name in diverging:
        print(f"    • {name}")
    
    print("  (See MATPLOTLIB_COLORMAPS list for all options)")
    
    print("\n" + "="*60)

# ==============================================================================
# SCIENTIFIC VISUALIZATION RECOMMENDATIONS
# ==============================================================================

# Based on research from matplotlib.org, Scientific Color Advice, and visualization best practices
RECOMMENDED_COLORMAPS = {
    # SEQUENTIAL DATA (magnitude, temperature, elevation, etc.)
    "sequential_best": [
        "viridis",      # Perceptually uniform, colorblind-friendly
        "plasma",       # High contrast, good for publications
        "inferno",      # Dark background friendly
        "cividis",      # Colorblind-optimized version of viridis
        "Blues",        # Intuitive for water/cold data
        "Oranges",      # Good for heat/warm data
    ],
    
    # DIVERGING DATA (anomalies, differences, deviations from mean)
    "diverging_best": [
        "coolwarm",     # Blue-white-red, excellent for temperature anomalies
        "RdBu_r",       # Red-blue reversed (red=warm, blue=cool)
        "RdYlBu",       # Red-yellow-blue, good contrast
        "seismic",      # High contrast diverging
        "Spectral_r",   # Rainbow-like but scientifically valid
        "bwr",          # Simple blue-white-red
    ],
    
    # PRECIPITATION/WATER DATA
    "precipitation_recommended": [
        "Blues",        # Intuitive: light=dry, dark=wet
        "BuGn",         # Blue-green transition
        "precipitation", # Your custom scheme (original)
        "jw_precip",    # Your custom scheme (enhanced)
    ],
    
    # TEMPERATURE DATA  
    "temperature_recommended": [
        "coolwarm",     # Blue=cold, red=hot (diverging)
        "RdYlBu_r",     # Red-yellow-blue reversed
        "temperature",  # Your custom scheme (original)
        "fire",         # Custom fire colors for heat
        "jw_temp",      # Your custom scheme
    ],
    
    # ELEVATION/TOPOGRAPHY
    "elevation_recommended": [
        "terrain",      # Brown-green-white (land-sea-snow)
        "gist_earth",   # Earth-like colors
        "earth_tones",  # Custom earth scheme
        "ocean_depth",  # Custom depth scheme (for bathymetry)
    ]
}

# Accessibility-focused colormaps (colorblind-friendly)
COLORBLIND_SAFE = [
    'viridis', 'plasma', 'inferno', 'magma', 'cividis',  # All matplotlib's new defaults
    'coolwarm', 'RdYlBu', 'Blues', 'Oranges', 'Greens'  # Good traditional choices
]

# High-contrast colormaps (good for presentations/posters)
HIGH_CONTRAST = [
    'plasma', 'inferno', 'magma',   # High dynamic range
    'seismic', 'coolwarm', 'bwr',   # Strong diverging contrast
    'Spectral', 'RdYlBu'            # Multi-color high contrast
]

def get_recommendations(data_type="sequential"):
    """
    Get colormap recommendations based on data type
    
    Args:
        data_type: Type of data visualization
                   Options: "sequential", "diverging", "precipitation", 
                           "temperature", "elevation"
    
    Returns:
        List of recommended colormap names
    """
    key = f"{data_type}_best" if data_type in ["sequential", "diverging"] else f"{data_type}_recommended"
    
    if key in RECOMMENDED_COLORMAPS:
        return RECOMMENDED_COLORMAPS[key]
    else:
        print(f"No specific recommendations for '{data_type}', using sequential defaults")
        return RECOMMENDED_COLORMAPS["sequential_best"]

def print_scientific_recommendations():
    """Print scientific colormap recommendations"""
    print("\n" + "="*70)
    print("SCIENTIFIC VISUALIZATION RECOMMENDATIONS")
    print("="*70)
    
    print("\n🔬 EVIDENCE-BASED COLORMAP CHOICES")
    print("Based on research from matplotlib.org, Scientific Color Advice,")
    print("and perceptual uniformity studies\n")
    
    for category, colormaps in RECOMMENDED_COLORMAPS.items():
        category_name = category.replace("_", " ").title()
        print(f"{category_name}:")
        for cmap in colormaps:
            accessibility = "🟢" if cmap in COLORBLIND_SAFE else "🟡"
            contrast = "📊" if cmap in HIGH_CONTRAST else ""
            print(f"  {accessibility} {cmap} {contrast}")
        print()
    
    print("Legend:")
    print("🟢 = Colorblind-friendly")
    print("🟡 = Check accessibility") 
    print("📊 = High contrast (good for presentations)")
    
    print("\n💡 QUICK RECOMMENDATIONS:")
    print("• General scientific data: viridis, plasma, cividis")
    print("• Temperature anomalies: coolwarm, RdBu_r") 
    print("• Precipitation: Blues, BuGn, your custom 'jw_precip'")
    print("• Elevation/terrain: terrain, gist_earth, earth_tones")
    print("• Publications: viridis, plasma (perceptually uniform)")
    print("• Presentations: plasma, inferno, seismic (high contrast)")
    
    print("\n⚠️  AVOID: 'jet' (rainbow) - proven problematic for science")
    print("   Better alternatives: viridis, plasma, Spectral")

# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================

if __name__ == "__main__":
    # Example usage
    print_available_colormaps()
    print_scientific_recommendations()
    
    # Test loading custom colormap
    try:
        precip_colors = get_custom_colormap("jw_precip")
        print(f"\nCustom colormap 'jw_precip' has {len(precip_colors)} color stops")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Test loading matplotlib colormap
    try:
        plasma_colors = matplotlib_to_blender_colormap("plasma", 10)
        print(f"Matplotlib colormap 'plasma' converted to {len(plasma_colors)} Blender color stops")
    except Exception as e:
        print(f"Error loading matplotlib colormap: {e}")
    
    # Show recommendations for different data types
    print(f"\nRecommendations for precipitation data: {get_recommendations('precipitation')}")
    print(f"Recommendations for temperature data: {get_recommendations('temperature')}")
