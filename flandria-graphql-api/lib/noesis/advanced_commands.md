Available options:
NOTE: Some of these may be broken or nonfunctional.
Most have not been tested in years.
Use at your own risk.
--------
-fmtidxlist - list format indices for use with -fmtoutidx/-imgoutidx/-animoutidx.
-quadtree # - quadtree encapsulation, with # recursion levels.
-nochop - do not chop meshes up into more meshes for quadtrees.
-smoothnorm # - smooth vertex normals with # unit tolerance.
-stexc - force half-shell spherical texture coordinates.
-forceskin n - force skin name for all objects to 'n'.
-posoffset # # # - translate all vertices by given offset.
-rotate # # # - transform all vertices by the given angles.
-scale # - scale all vertices on the model, where # is the scale factor.
-transleg - legacy joint transforms, incompatible with some exporters.
-recenter - re-centers entire model.
-noanims - skip all animation writes/exports.
-nogeo - skip all geometry writes/exports.
-notex - skip all image/texture writes/exports.
-renamebone <from> <to> - renames a bone.
-brot <name> # # # - rotate bone <name> by # # # (xyz euler angles).
-brem <name> - removes bone <name> from skeleton.
-bmoda - enables brot and other bone transforms on anim data.
-bakeanimscale - bakes skeletal anim scale (frame 0) into vertex data.
-bakeposescale - bakes base pose scale into vertex data.
-removeskelscale - removes scale from all skeletal transforms.
-matlerp # - # specifies matlerp type, 0=matlerp 1=quatslerp.
-forcetc - force texture coordinate data chunk to be written.
-ignoreroot - ignore root movement. (animations only)
-vertclr - forces vertex color chunks into all meshes.
-vertalpha - fade alpha colors on verts based on z coordinate.
-vertcull # # # - vert cull with pos, uv, and color thresholds.
-flipuv - flips uv y coordinate.
-flipuvidx # - flips uv y coordinate on channel #.
-flipuv1m - change uv flip method.
-flipax # - flip pos/nrm on axis # where # is 1-3 (x-z).
-combinemeshes - combines meshes when possible.
-decim # - new decimation, # should be 0-1. (0=no detail, 1=full)
-nopause - no pause when done. (for batch processing)
-noskel - does not export vertex weight or bone information.
-animcomp # - anim pos/quat compression. 1=shorts, 2=bytes, 3=dynamic.
-skinar - outputs precomputed vertex skin arrays for each mesh.
-killdupfaces - removes duplicate faces.
-idxopt - index order optimization.
-idxopt2 - alternate index order optimization.
-idxsort - sort interleaved index arrays based on texture/lm index.
-stripper - strip order index sorting.
-stripper2 - alternate strip order index sorting.
-stripper3 - write actual strips instead of lists.
-vorder - re-sort vertices in order of index references.
-edgewelder # - welds triangle edges, where # is a unit tolerance.
-hiefrombones - attempt to establish mesh hierarchy from skel + weights.
-maxbones # - a single mesh cannot reference more than this many bones.
-maxvertweights # - a single vert cannot have more than # weights.
-maxverts # - split meshes with more than # verts.
-maxtris # - split meshes with more than # tris.
-decalmesh - generates rendermodel collision/decal meshes.
-loadanim <file> - loads animation from a file, to export with main data.
-loadanimsingle <file> - loadanim, but keep metadata/sequences. (no concat)
-loadanimscale <file> - Same as -loadanim but re-applies scales.
-texpre <string> - prepends to used texture names when exporting lzs/ghoul2.
-bonecull - cull unreferenced bones.
-bonemap <file> - specifies a .bma file to lay out a complete skeleton.
-bonemapex - exports a .bma for model being exported if a skeleton exists.
-modelindex # - extracts sub-model #, if more than one model in file.
-texexsel - export only textures in the selected model.
-animexall - export all animations, even outside of the selected model.
-toonshell # - creates toon shell meshes extruded to # units.
-showstats - prints detailed final chunk memory info.
-listen # - server processing mode, listen on port #.
-align # - ensure #-byte alignment for each chunk.
-vertbones - generates per-vertex bones, derives anims from vert anims.
-morphframe # - replace static geo with morph frame #.
-animbonenamematch - force name-based matching even if bone counts match.
-imgresz # # - resizes all images to #x#.
-imgcrop # # - crops all images to #x#. (from upper left)
-imgcropio # # - as above, cropping from image origin.
-imgcroplr # # - as above, cropping from lower right.
-imgcroprect # # # # - as above, cropping to rect. (x0, y0, x1, y1)
-imgbicubic - forces bicubic resampling instead of bilinear.
-imgbicubicmin - forces bicubic resampling instead of bilinear, only for minification.
-imgtcont # - in bicubic resampling, enables tcb eval and specifies continuity. should be 0..1.
-imgmcut # - applies median cut to # colors to all images.
-texnorepfn - does not replace first tex filename with output.
-texexidx # - starts texture export from index #.
-texexcnt # - only export # textures, if more exist.
-nofmtexopt - disables format-specific export options, handle with care.
-arcnooverwrite - enables overwrite checking for archive extraction.
-rpgforcesort - force RPG bucket sort.
-rpgsanweight - force RPGOPT_SANITIZEWEIGHTS.
-rpgswaphand - force RPGOPT_SWAPHANDEDNESS.
-exportprvtex - export textures that were only loaded for preview.
-fulltexpath - force full texture path when exporting textures.
-forcedeppath <path> - write dependencies (textures, anims) on path.
-forcedeppathrel <path> - as above, but path relative to output.
-prvdatapath - force preview data/load path on standard export.
-enablefslwr - enable legacy fs path lowering. inconsistent between formats.
-convertlegacylm - convert legacy lightmaps to multi-pass materials.
-paltransindex # - specify palette transparency by index.
-paltranscolor # # # - specify palette transparency by rgb.
-nopreviewtex - disabled preview texture loading.
-animfilter <name> - filters anim export by name, may use more than once.
-logfile <path> - log all output to <path>.

Module-specific commands
--
Various BSP
-bspclip - optimizes bsp input models for clipping.
-bspleafmerge - uses reference leafs to merge leaf surfaces.
-bsprebsp # - re-bsp q1/hl bsp's in rcube format with # spatial divisions.
-bsplvec <filename> - pulls lightmaps from another bsp for light normals.
-bspdeluxe - specifies input bsp has light vectors in top half of lightmaps.
-bspdelswap - swaps top and bottom lightmap sets for deluxels.
-bsplmsize # - force expected bsp import lightmap size to #x#.
-bsplmresize # - combined lightmap pages to #x#.
-bspwad <filename> - specifies wad2/wad3 file for q1/hl bsp textures.
-bsptexout - outputs png files for q1/hl bsp textures.
-bsplg # # # - override procedural lightgrid dimensions for q1/hl bsp.
-bsplmul # - lightmap multiply by #.
-bspgengrid - generate lightgrid from lightmap for q1/hl bsp.
-bspnotree - ignore tree in q3bsp.
-lgfix - re-samples out-of-leaf lightgrid samples on q3bsp import.
-extlm - if lightmap is presented, make it external.

MAP
-mapquake - parse map in quake instead of half-life format.
-mapbnames - name brushes to avoid geometry merging.

MDL/MD2/MD3
-mdlskinscl - auto-resizes mdl skins with more than 200 vertical pixels.
-mdlskinsize # # - auto-resizes mdl/md2 skins to #(width) * #(height).
-mdlavoidfb - avoid fullbright pixels in mdl skins.
-mdlexportfg - export framegroups if available.
-mdladdskin - add skin to export to mdl.
-mdlnobase - don't include base pose in mdl frames.
-mdlflags # - sets mdl header flags to #.
-md2strips - invoke the stripper for md2 glcmd output.
-md2painskin - add an additional pain skin for md2 output.
-md3tag <string> - sets default md3 tag name.
-md3tbone <string1> <string2> - md3 tag string2 from bone string1.

FF7
-ff7weapon # - only export this weapon model (0-15) and not all.
-ff7weaponbone # - attach the weapon model(s) to this bone number.
-ff7weaponrot # # # - transform weapon(s) by given angles.
-ff7weapontrans # # # - transform weapon(s) by given offset.
-ff7batch - batches vertex color surfaces into one, using bone weights.
-ff7pot - resizes output tim->png textures to power of two.
-ff7notrim - do not eliminate overlapping triangles.
-ff7texnudge # - nudges textured surfaces by # units along normal.
-ff7boneremap # # - remaps bone index # to second #.

FF8
-ff8animscale - use scales in animation data.

MPO
-mpo3ds - use 3ds-specific header for mpo export.

GMO
-gmononorm - ignores gmo normals.
-gmogroup - groups gmo surfaces by material.
-gmobasepose - gmo base pose export.
-gmokeeptexnames - keep original texture names.

Dreamcast Ninja Formats
-pvppalbank # # - specify colors per bank (first #) and bank index to load from pvp.

SC5
-sc5altfile - force alt file load.

SMD
-smdomittexpath - omit assets/textures/ path for smd materials.
-smdoldtexexportnaming - include path/etc. in smd material name.
-smdoldparsing - old-style parsing.
-smduseactualmatname - use real mtl name on export, not diffuse.
-smdnonorm - ignore smd normals.
-smdmultiseq - export sequences as multiple smd files.
-smdmeshnodes - create nodes for mesh containers.

Source MDL
-srcmdlnovmt - don't attempt to load vmt files for textures.
-srcmdlpbr - force PBR shading model on materials.
-srcmdlforcebmap - force use of bonemap if present.
-srcmdllod # - load lod #. default 0.

DMC4/RE5/LP Model
-capmodln1 - ignore everything except lod -1 objects.

ISO
-isokeepsemi - keeps semicolon for version part of filename.
-isoxdvdscan - tell the iso handler to scan the image for xdvdfs.

RDM
-disposable - sets disposable instance flag for output rdm.
-vertilv - output special interleaved vertex format.
-vertilvlm - no color/normal for interleaved lightmapped surfs.

3DS
-3dsnotex - no texture loading.
-3dsnotproc - no material-based texture processing.
-3dsnocconv - don't convert material colors to linear space.
-3dsnoanim - don't parse animation data.
-3dsnosmooth - don't calculate normals from smoothing groups.
-3dsanimrange - only evaluate frames for file's anim range.
-3dsnoreadcam - don't read camera/target/light/etc. transforms/data.
-3dsdischid - discard hidden meshes.
-3dsnoease - don't apply ease in/out to key interpolation.
-3dsforcelerp - force linear interpolation of animation curves.

WaveFront OBJ
-objmtl - enables export of mtl file with the obj.

DDS
-ddsati2nonorm - don't derive+renormalize when decoding DXT ATI2/BC5.
-ddsnohdr - don't write HDR foramts via fourcc-DX10.

DOAX2/NG2 Model
-tprnormaltex - attempt to auto-assign normal maps.

FF13
-ff13cclamp # - hdr color scale clamp. default 1.5.
-ff13cscale # - hdr color scale. default 1.0.
-ff13ascale - if invoked, enables ff13 anim scale.
-ff13mgamma - enables gamma correct lighting on ff13 materials.

PNG Image
-pngpal - prefer paletted png output, if palette provided.

Autodesk FBX
-fbxexportver <arg> - exports explicit fbx version <arg>, e.g. FBX201400, FBX201600.
-fbxoldexport - exports legacy fbx format instead of current.
-fbxmeshmerge - merges meshes based on source name on export.
-fbxmeshmergemv - only allow merges if vert layouts match.
-fbxaffinenodes - evaluate nodes as affine transforms.
-fbxzup - sets the scene axis to z up on export.
-fbxsmoothgroups - generate smoothgroups from vertex normals on export.
-fbxtexrelonly - only set relative paths for texture filenames.
-fbxnoflipuv - don't flip uv on import/export.
-fbxnovcolor - ignore vertex colors on import.
-fbxtexrel - use relative texture filenames.
-fbxlegacycluster - use legacy cluster transform logic.
-fbxnoblendshapes - don't import or export blendshapes.
-fbxbsnonormals - don't use blendshape normals.
-fbxpreserveprops - preserve all relevant property data.
-fbxoldprop - old property iteration. (fbx sdk bug)
-fbxmultitake - export a take for each anim sequence.
-fbxbonestomeshtf - derive mesh transforms from bones, and don't write bones.
-fbxpreservecp - does not allow welding between controlpoints.
-fbxnooptimize - disables fbx geometry optimization pass.
-fbxnoesidecar - enables .noefbx sidecar files to preserve extra data.
-fbxcanimtime - use curve key times instead of clamped evaluator time.
-fbxsortnodes - sort nodes alphabetically on import.
-fbxmtlfrommeshname - create materials from mesh names.
-fbxunifybi <arg> - unifies binormals on import. (0=no, 1=yes, 2=flipped)
-fbxrottan - rotates tangent/binormals on import.
-fbxnotan - disables reading/writing tangents for fbx.
-fbxnoextraframe - avoids adding an extra frame for timing.
-fbxframecount <arg> - overrides the fbx anim frame count.
-fbxframerate <arg> - specifies the fbx framerate. (frames per second)
-fbxtexext <arg> - appends given value to texture names on export.
-fbxscalehack - transform override for scale correction.
-fbxforcetri - force triangulation on import.
-fbxadjustcoords - adjust coordinate system on import.
-fbxnoscale - force normalization of all transforms.
-fbxnosceneunitcor - no scene unit correction on import.
-fbxnoskintoworld - don't skin geometry to bones in world space.
-fbxtritopoly <arg> - tris to polys, <arg> is max degrees for combine.
-fbxtritopolyconctol <arg> - <arg> is concavity tolerance.
-fbxcollapsecp - collapse controlpoints.
-fbxdixhax <arg> - various hacks just for me!
-fbxreducekeys - reduce animation keys.
-fbxnonlinrot - specifies nearest snap for rotations.
-fbxnomeshhierarchy - no separate udcommon mesh hierarchy.
-fbxnomeshbones - no bones generated from mesh nodes.
-fbxascii - exports fbx as ascii instead of binary.
-fbxpasswd <arg> - specifies the password for an encrypted fbx.

Bayonetta/PG Model
-bayopgnomathack - disable bayonetta material hack.
-bayopgnofuse - disable level models fusion.
-bayopgfuse - enable level models fusion.
-bayopgnoexternal - disable external processing tools.
-bayopgexternal - enable external processing tools.
-bayopgnolods - disable LODs.
-bayopglods - enable LODs.
-bayopgnoshadows - disable shadow meshes.
-bayopgshadows - enable shadow meshes.
-bayopgnolightmaps - disable lightmaps.
-bayopglightmaps - enable lightmaps.
-bayopgnomultipass - disable bayonetta multi-pass materials.
-bayopgmultipass - enable bayonetta multi-pass materials.
-bayopgnotexprompt - disable prommpt for external/shared textures.
-bayopgtexprompt - enable prommpt for external/shared textures.
-bayopgnoanimprompt - disable prompt for external animation.
-bayopganimprompt - enable prompt for external animation.

Duke Nukem Forever Model
-dnfpbrmaterials - use pbr materials.
-dnfclipanimtime - clip anim sequence time by keyframe.
-dnfanimframerate <arg> - specify framerate for anim - default 30.
-dnfaddanim <arg> - combine animation. (only applies to anim files)

Doom Wad
-wadmapindex <arg> - only load a particular map specified by index.
-wadsprcsize <arg> - specifies fixed sprite canvas size.
-wadloadspr - load sprites as textures.
-wadopensec - generate geometry for open sectors.
-wadconvex - assumes convex subsector data instead of regenerating.
-wadnogl - disables parsing glbsp lumps and looking for gwa file.
-wadmincut <arg> - minimum dist to chop convex subsect poly.
-wadweldverts <arg> - welds map verts with # threshold.
-wadcollapseedges <arg> - collapses map edges with # threshold.

GIF Image
-gifnoalpha - disables alpha masking on gif import.
-gifdelay <arg> - specifies interval between frames in exported file.
-gifhold - prevents gif animation from looping in exported file.

EXR Image
-exrnogamma - don't convert ldr data to gamma space on import.

BioVision Hierarchy Anim
-bvhnosortbones - don't sort bones. sorting may break bone index matching, not sorting may produce unloadable bvh files.

PKM Image
-pkmetc2 - force etc2 encoding.

Gamebryo NIF
-nifnoanim - don't load animation components.
-niferpangles - interpolate angles instead of converting to quaternions.
-nifnoversionhacks - don't use version hacks.
-nifusevcolors - uses vertex colors.
-nifnotransform - doesn't perform geometry transform into skeleton space.
-nifforcenodenames - forces node/bone names to node#.
-nifnostaticweights - if invoked, static geometry will not be weighted to mesh nodes.
-nifpbrtest - test pbr materials, when applicable.
-niflmindex <arg> - specify texture index to treat as lightmap.
-nifforceenv <arg> - force env texture on all materials to <arg>.
-nifloadskel <arg> - map skeleton from another nif, loaded from path <arg>.

GoldenEye N64 Model
-ge64head <arg> - loads a head model.
-ge64minlod <arg> - ignore nodes with min lod dist > <arg>.

GoldenEye N64 Animations
-ge64anmflip - use alternate direction mapping.
-ge64anmmdl <arg> - specify model to pair with animation.

Quake II BSP
-q2bsplmscl <arg> - scale lightmap colors by <arg>.

Quake II WAL Texture
-walname <arg> - <arg> is internal name for wal
-walanim <arg> - <arg> is next anim frame name for wal

M32 Image
-m32name <arg> - <arg> is internal name for m32
-m32detail <arg> - <arg> is internal detail tex for m32

UE4 Asset
-ue4datapath <arg> - scan <arg> recursively for export data.
-ue4animref <arg> - specifies skinned mesh for anim reference.
-ue4anims - attempt to load animations.
-ue4bidx - name bones by index.
-ue4parseemsv - parse emissive textures from material by name.
-ue4sanity - sanity-check list counts.
-ue4nosecname - don't name meshes by section.
-ue4defaultmtl - force default material names.
-ue4texalign <arg> - align textures to <arg>.
-ue4texgobstd - use standard mip0 block height selection. (switch)
-ue4texgob - force texture untiling. (switch)
-ue4tex1dalign - force typical ps4 1dthin untiling rules.
-ue4tex1dthin - force texture untiling. (ps4)
-ue4gamehack <arg> - force gamehack to <arg>. see UE4_GAMEHACK_*.
-ue4serialver <arg> - force serialization version to <arg>. see UE4_SERIALVER_*.

Ultima Online Map
-uomapterrain <arg> - renders map in region <arg>, formatting is x;y;w;h.

Half-Life MDL Model
-hlmdluseseqgroups - tries to use sequence group offsets.
-hlmdlnonrm - discards normals for hl models.

FF11 Model/Data
-ff11blendhack <arg> - sw render to determine alpha coverage, <arg>=min frac.
-ff11bumpdir <arg> - specify directory for bump textures.
-ff11hton <arg> - convert height to normal maps, arg=z factor.
-ff11optimizegeo - remove degenerates and redundant verts.
-ff11nolodchange - don't try to switch to lod0.
-ff11mapbones - create bones for map objects.
-ff11keepnames <arg> - 1=keep map object names, 2=w/index prefix, 3=w/subobj.
-ff11renderunref - render unreferenced map geo at identity.
-ff11forcelighting - force lighting.
-ff11forcecull - force culling.
-ff11novertcolor - no vertex colors.
-ff11noshiny - no special assignment for shiny materials.
-ff11shiftvertalpha <arg> - explicitly shift vert alpha <arg> bits.
-ff11shiftvertcolor <arg> - explicitly shift vert color <arg> bits.
-ff11shiftcolor <arg> - explicitly shift tex color <arg> bits.
-ff11shiftalpha <arg> - explicitly shift tex alpha <arg> bits.

FF11 SQLE Model
-ff11sqleanim <arg> - load sqle animation <arg> as relative path.

FF12 Model
-ff12ascale - apply ff12 anim scales.
-ff12animadd - applies base pose with additive animations.
-ff12nodraw - ignores draw lists for ff12 models.

FF15 Model
-ff15loadlods - load all lod's.
-ff15pickanim - when loading a model, look around and try to load a random clip.
-ff15noskel - don't attempt skeleton load.
-ff15nospecoccl - don't apply spec occlusion when using -ff15materials.
-ff15occlmap - try to load occlusion maps. requires -ff15materials.
-ff15materials - attempt actually load materials.
-ff15notex - don't attempt to load textures.
-ff15repna - reparent joints outside of the animation hierarchy.
-ff15lowtex - don't prefer _$h textures.
-ff15trnonsphere - force translations to conform to a sphere.
-ff15trnscl <arg> - scale translations.
-ff15addanim - apply animation as additive.
-ff15noscale - don't apply scale.
-ff15notrn - don't apply translation or root motion.
-ff15chp <arg> - supply interim channel pad.
-ff15softhair - force self-sorting soft hair.

Quake Saturn LEV
-qsattexdeq <arg> - specify texture color dequantization mode. (0-2)
-qsatnosky - don't create visible poly planes for sky.
-qsatsubcolor - use subtractive vertex colors.
-qsatenabletexfilter - enable texture filtering.
-qsatwelddist <arg> - specify edge/point weld for re-projected tiles.
-qsatcoplofs <arg> - specify offset distance for intersecting coplanar surfaces.

LiDAR (LAS) Model
-lasnocolor - no point color data.
-lasaspoints - interpret as point cloud.

Battlezone GEO Model
-bzoneoverparse - over-parse geo chunks for additional geo.
-bzoneskipclass <arg> - skip objects of <arg> type.
-bzonepaltindex <arg> - specifies the palette index for transparency.
-bzonepal <arg> - specifies the palette for .map exports.
-bzonedeftexex <arg> - specifies default target texture extension.
-bzonekeepclr - keep color/transparency in vertex color channel.

Radiance HDR
-hdrnorle - no RLE encoding.
-hdrnogamma - no conversion between gamma/linear on import/export.

SotN Zone
-sotnnodeftile - don't draw default tiles.
-sotnseplayers - each layer as a separate texture.

JPEG 2000 Image
-j2kchansplit - treat each channel as separate image.
-j2kchanskip <arg> - skip channels.
-j2kchanstart <arg> - provide explicit channel start index.
-j2kbias <arg> - provide explicit channel bias.
-j2knoshift - no quantization shift.
-j2khdr - preserve HDR image data.
-j2krate <arg> - specifies encoding rate.

GHOUL2 Model
-g2exalwaystform <arg> - sets always-transform flag on bone <arg>.
-g2exanimconfig - write animconfig for gla if sequence data present.
-g2extagtrivertshift <arg> - shifts tag triangle vertex indices by <arg>.
-g2extrivertshift <arg> - shifts non-tag triangle vertex indices by <arg>.
-g2exforceskeleton <arg> - forces <arg> bone count for glm export.
-g2exbasematrixscale <arg> - scale for base gla matrices.
-g2exbasetranslationscale <arg> - scale for base gla translations.
-g2exmatrixscale <arg> - specifies scale applied to gla matrices.
-g2extranslationscale <arg> - specifies scale applied to gla translation.
-g2exreportscale <arg> - specifies scale written to gla header.
-g2exorderbonesfromgla <arg> - filename of gla to use for bone order.
-g2exanimname <arg> - specifies exported anim name.
-g2exmodelname <arg> - specifies exported model name.
-g2exmultiroots - allow multiple unparented surfs.
-g2exfakehierarchy - fake hierarchy on glm export.
-g2exforceshader <arg> - force shader name, <arg> 1=from material, 2=none.
-g2skinname <arg> - specifies a non-default .skin file.
-g2noskinfiles - disable use of .skin files.
-g2skipsurf <arg> - does not export surface <arg>.
-g2normalizemats - normalize bone mats.
-g2skiptag - skips tag surfaces.
-g2skipoff - skips off surfaces.

GHOUL Model
-ghbgz - enable GZ_ surfaces.
-ghbgpm <arg> - specify a gpm file.
-ghbmatpbr - use PBR materials.
-ghblogseq - log sequence information.

KVX Voxel Model
-kvxmarchfile <arg> - <arg> specifies a .noevmarch config file for marching.
-kvxvfile <arg> - <arg> specifies a .noevox config file for voxelization.
-kvxloadmip <arg> - <arg> specifies a mipmap index, for kvx files with mips.
-kvxnomips - disables writing additional mips for kvx export.
-kvxnobreak - don't break slab run when cull flags change.
-kvxpadunits <arg> - pad grid units by <arg>.
-kvxoptimize - perform post-submit mesh optimization.
-kvxnoflood - avoids floodfill to cull backfaces.

VOX Voxel Model
-voxmarchfile <arg> - <arg> specifies a .noevmarch config file for marching.
-voxvfile <arg> - <arg> specifies a .noevox config file for voxelization.
-voxoptimize - perform post-submit mesh optimization.

MRI - Analyze 7.5
-analyzeflat - generate 2d image slices instead of volume mesh.
-analyzecolor <arg> - color from intensities, <arg> is color mode.
-analyzemarchfile <arg> - <arg> specifies a .noevmarch config file for marching.

MRI - DICOM
-dicommarchfile <arg> - specify march config file as <arg> for volume set.
-dicomelemlog <arg> - log all data elements, <arg> is verbosity level.
-dicomsetwindow <arg> - apply and set window, args=width;center;ymin;ymax.
-dicomapplywindow - apply window given in file.
-dicomapplyslope - apply slope and intercept (e.g. convert to Hounsfield units) to data.
-dicomdatanormalize - normalize values to data type extents.
-dicomsbp <arg> - <arg> should be in the form of scale;bias;exponent.
-dicomfltnrm - normalizing floating point image data.

Duke3D Map
-dukemapspritemode <arg> - where 0=non-effectors, 1=all, 2=none.
-dukemapskippara - skip parallax ceiling/floor/wall draws.
-dukemapnamesecs - name ceilings/floors/walls after sectors.
-dukemapnofudge - don't fudge wall/floor sprite positions.
-dukemaptnoalign - no alignment of wall tile heights.
-dukemapshtable - make use of the shading table instead of approximating via vert colors.

Plague Tale Model
-ptaleanimscl <arg> - specify anim scale mode.
-ptalenotrn - disable animation translation.
-ptalenomapbones - no bones from map nodes.
-ptalelod <arg> - preferred lod for map objects.
-ptalemeshhonly - only include hash in mesh names.
-ptalemeshnodes - for maps, prefix mesh name with node.
-ptalekeepbb - keep billboard/volume geometry in map.
-ptalenomorph - don't load morphtargets.
-ptalenotex - don't load textures.
-ptaleanimmdl <arg> - force model to load with anm files. path is local to anm.
-ptaleskel <arg> - force skeleton to be loaded with msh files. path is local to msh.

RW DFF (very old version)
-dff1split - split meshes by group.
-dff1nomask - don't alpha-mask textures.
-dff1bone - create bones for transforms where possible.

Roomba Model
-roombaremseg <arg> - seg removal type.
-roombaareahint <arg> - hint max area size.
-roombauvscale <arg> - uv scale.
-roombanogeo - no object geo.
-roombanocuts - no object cuts.
-roombaceilz <arg> - ceiling z.
-roombaobjz <arg> - object z.
-roombacoldis <arg> - collapse distance.
-roombaharden <arg> - hardening value.
-roombasamalt - alt sampling.
-roombasamexp <arg> - sample exponent.
-roombasamrad <arg> - sample radius.
-roombamscale <arg> - map scale.
-roombamshift <arg> - map shift.
-roombainterp <arg> - 0=geo, 1=image

glTF Model
-gltfmeshgroup <arg> - regroup meshes on export. 1=by source name, 2=all.
-gltfmirror - mirror x axis on import. (not export)
-gltfnonoeex - don't write noesis extensions.
-gltfdiscnoren - discard meshes with skip-render materials.
-gltftranscene - apply format-dependent scene transform.
-gltfnometalhack - don't set min metal based on metal mat flag.
-gltfoneanim - force all sequences to be shoved into a single anim.
-gltfnoared - disable animation key reduction.
-gltfnotexp - disable texture processing for spec/normal.
-gltfkeepmeshnodes - create bones for noesis mesh nodes on import.
-gltfskrefn - only make bones for skin-ref nodes.
-gltfnogloss - don't use glossiness mat ext.
-gltfnorgdwgt - don't generate skin weights for unskinned mesh nodes.
-gltfnoenv - don't auto-load default envmap.
-gltfmorphs - enable loading morph targets as vertex anim frames.
-gltfanimrate <arg> - anim sample rate.
-gltfdrawunref - draw any meshes not referenced by nodes.
-gltfkeepbind - don't transform geometry to fit nodes.
-gltfscene <arg> - explicitly select scene.

Messiah Model
-msiahanimfilter <arg> - only load the animations under this path.
-msiahfrcact <arg> - force actor name for anim lookup.
-msiahtblack - make black in texture(s) transparent.
-msiahlerp - lerps verts instead of snapping.

Quake II PSX Proto Editor Model
-q2edmrgb - use embedded rgb values.
-q2edmnotweak - don't use polygon tweak indices.

Quake II PSX Model
-q2psxnotofs - disable half-texel offset.
-q2psxtalpha - use texture alpha.
-q2psxtpal <arg> - specify palette transparency index.

Chopper Mega Drive
-chopmdlabel <arg> - only parse a particular label prefix.
-chopmdbgclr - don't try pal0 as transparent black.

DeluxePaint Image
-ilbmchunkalign <arg> - specify chunk alignment, default 2. (must be pow2)
-ilbmrowalign <arg> - specify image row alignment, default 16. (must be pow2)
-ilbmloadpal <arg> - load palette for export.
-ilbmcompress - compress output.
-ilbmanimilv <arg> - force interleave value. should usually be 2, some files misreport.
-ilbmanimt5xor - obey (often erroneous) xor flag for mode 5.
-ilbmpbm - write PBM-format instead of ILBM.
-ilbmnoanimdrop - don't drop anim reference frames.
-ilbmtruecolor - write true color image instead of paletted.

DeluxePaint Animation
-dpanimexkeepidx - always use original paletted indices, if available.
-dpanimexpal <arg> - load palette on export.
-dpanimexheight <arg> - force height on export.
-dpanimexwidth <arg> - force width on export.
-dpanimexnocomp - don't compress data.
-dpanimexnodelta - don't write delta frame.
-dpanimexnocut - no median cut on export.
-dpanimkeepdelta - keep delta frame on import.
-dpanimpalrng <arg> - specify opaque palette range in form of min_max.
-dpanimfindrect - crop sequence according to single-line rectangle.

Digitizer III Image
-pet3bnopair - don't prompt for paired model when encountering anims.
-flcignorepack - ignore packet count in byterun.
-flckeepring - keep ring frame.
-dig3chack - use same color hack as dig2lbm.
-dig3tcolor <arg> - force transparency by plaette color. (r;g;b)
-dig3tindexmask <arg> - mask for palette index when checking tindex, e.g. 15.
-dig3tindex <arg> - force transparency by plaette index.
-dig3mincanv - force minimum 320x224 canvas.
-dig3canv - put all pieces on a single canvas.

Animator FLC Image
-flctindex <arg> - force transparency by palette index.

Dead Cells Sprites
-dcatlclipframes - clip unused x/y across all frames.
-dcatlnooffset - no frame offsets.
-dcatluseorigin - use atlas frame origins.
-dcatlprefix <arg> - only process frames with given prefix.

Chasm CAR Model
-chasmloadmodels - load additional map models.
-chasmnosky - don't draw sky surfaces.
-chasmnosub - don't load submodels.
-chasmkeep255 <arg> - don't use transparent pal entries. (applies to cel)

Inter-Quake Model
-iqmpreserveseq - preserve sequences upon import and export.

EF/Raven MDR
-mdrvertlocal - puts verts in bone-local space, preserves skeleton.
-mdrbtag <arg> - <arg> should be "bonename;tagname" to add a tag.
-mdrforcebonemspace <arg> - forces bone <arg> to be in model space.
-mdrnocomp - don't compress anim frames on export.
-mdrnoboner - don't relocate bones on import.
-mdrdefpose - special default pose import with no anims.

Unreal ActorX Model
-pskkeepspace - keep trailing spaces in bone names.

