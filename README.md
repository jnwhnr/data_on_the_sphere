# data on the sphere

<img width="300" height="300" alt="t2m_JJA_Himalayas_wow_zoom055_-10_+40_colorbar" src="https://github.com/user-attachments/assets/e326a313-ff24-4776-8b99-6dc481fabd54" />
<img width="300" height="300" alt="tp_scaling_DJF_Europe_wow_zoom00_-1 2_+1 2_colorbar" src="https://github.com/user-attachments/assets/9b212d25-a654-46f2-93ad-3ed44b9693b7" />


## install requirements

### for the scripts

You can use the `pixi.toml` file do install dependencies.

### install blender dependencies

It might be necessary to install matplotlib and pillow into the blender env by hand (adjust blender version to what you use):

```
/Applications/Blender.app/Contents/Resources/4.5/python/bin/python3.11 -m pip install matplotlib pillow --target /Applications/Blender.app/Contents/Resources/4.5/python/lib/python3.11/site-packages
```


## run with

### tp
```
/Applications/Blender.app/Contents/MacOS/Blender -b -P render_sphere.py -- HR1279_prec_scaling_DJF.tiff presentation --variable tp_dif --vmin -1.2 --vmax 1.2 --locations Europe,Himalayas --effects --do-overlay --overlay-theme dark --overlay-opacity 0.8
```
### t2m
```
/Applications/Blender.app/Contents/MacOS/Blender -b -P render_sphere.py -- HR1279_t2m_2002_2012_JJA.tiff presentation --variable t2m --vmin -30 --vmax 30 --locations Europe,Himalayas --zoomlevel 0.55 --effects --do-overlay --overlay-theme light --overlay-opacity 0.3

```

## The tif file

The tiff file needs to be a float32 tiff that is projected in Plate-Caree (lat-lon, epsg:4326) and covers the whole globe. 
Longitude should be from -180 to 180.

You might be able to generate it like this, for example:

```python
ds = xr.open_mfdataset("your_data.nc")
variable = ds["t2m"].astype('float32')
variable.rio.to_raster("your_data.tif", driver="GTiff", compress="LZW")
```



## Arguments

**Required:**
- `input_tiff` - Input TIFF file path
- `output_dir` - Output directory path

**Optional:**
- `--resource` - Resource parameter
- `--locations` - Comma separated locations (default: "Europe")
  - Available: `Africa`, `Europe`, `Asia`, `North_America`, `South_America`, `Australia`, `Arctic`, `Antarctica`, `Marrakech_Atlas`, `Congo_River`, `Himalayas`, `Bremen`
- `--variable` - Variable type (default: "t2m")
  - Available: `t2m`, `tp`, `tp_dif`, `t2m_dif`, `ocean_depth`, `earth_tones`, `fire`, `viridis`, `plasma`, `inferno`, `magma`, `cividis`, `Blues`, `BuGn`, `BuPu`, `GnBu`, `Greens`, `Greys`, `Oranges`, `OrRd`, `PuBu`, `PuBuGn`, `PuRd`, `Purples`, `RdPu`, `Reds`, `YlGn`, `YlGnBu`, `YlOrBr`, `YlOrRd`, `coolwarm`, `bwr`, `seismic`, `RdBu`, `RdGy`, `RdYlBu`, `RdYlGn`, `Spectral`, `BrBG`, `PiYG`, `PRGn`, `PuOr`, `twilight`, `twilight_shifted`, `hsv`, `flag`, `prism`, `ocean`, `gist_earth`, `terrain`, `gist_stern`, `gnuplot`, `gnuplot2`, `CMRmap`, `cubehelix`, `brg`, `gist_rainbow`, `rainbow`, `jet`, `nipy_spectral`, `gist_ncar`
- `--vmin` - Minimum value (default: 0)
- `--vmax` - Maximum value (default: 10)
- `--do-overlay` - Enable overlay
- `--overlay-theme` - dark and light (default: light)
- `--overlay-opacity` - Overlay opacity (default: 0)
- `--zoomlevel` - Zoom level (default: 0)
- `--dof` - Enable depth of field
- `--effects` - Add special effects like glow
- `--lowres` - Use low resolution
