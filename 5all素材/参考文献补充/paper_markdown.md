C:\Users\deerfeifei\AppData\Local\Programs\Python\Python312\Lib\site-packages\pydub\utils.py:170: RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work
  warn("Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work", RuntimeWarning)
This CVPR Findings paper is the Open Access version, provided by the Computer Vision
Foundation. Except for this watermark, it is identical to the accepted version;
the final published version of the proceedings is available on IEEE Xplore.
Exploring the best way for UAV visual localization under Low-altitude
|     |     | Multi-view |     |     | Observation |     | Condition: | a Benchmark |     |     |     |     |
| --- | --- | ---------- | --- | --- | ----------- | --- | ---------- | ----------- | --- | --- | --- | --- |
YibinYe1* XichaoTeng1* ShuoChen1 LeqiLiu1 KunWang1 XiaokaiSong1 ZhangLi1,(cid:2)
1NationalUniversityofDefenseTechnology,China
|     |     |     |     |     |     | zhangli | nudt@163.com |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | ------------ | --- | --- | --- | --- | --- |
Abstract
| Absolute            | Visual | Localization | (AVL)        | enables   | an       | Unmanned  |     |     |     |     |     |     |
| ------------------- | ------ | ------------ | ------------ | --------- | -------- | --------- | --- | --- | --- | --- | --- | --- |
| Aerial Vehicle      |        | (UAV) to     | determine    | its       | position | in GNSS-  |     |     |     |     |     |     |
| denied environments |        | by           | establishing | geometric |          | relation- |     |     |     |     |     |     |
shipsbetweenUAVimagesandgeo-taggedreferencemaps.
| While many     | previous   | works      | have        | achieved       | AVL      | with im-   |     |     |     |     |     |     |
| -------------- | ---------- | ---------- | ----------- | -------------- | -------- | ---------- | --- | --- | --- | --- | --- | --- |
| age retrieval  | and        | matching   | techniques, |                | research | in low-    |     |     |     |     |     |     |
| altitude       | multi-view | scenarios  | still       | remains        | limited. | Low-       |     |     |     |     |     |     |
| altitude       | Multi-view | conditions |             | present        | greater  | challenges |     |     |     |     |     |     |
| due to extreme |            | viewpoint  | changes.    | To investigate |          | effective  |     |     |     |     |     |     |
UAVAVLapproachesundersuchconditions,wepresentthis
| benchmark. | Firstly, | a large-scale |     | low-altitude |     | multi-view |     |     |     |     |     |     |
| ---------- | -------- | ------------- | --- | ------------ | --- | ---------- | --- | --- | --- | --- | --- | --- |
datasetcalledAnyVisLocwasconstructed.
Thisdatasetin-
| cludes 18,000 | images | captured |     | at multiple | scenes | and al- |     |     |     |     |     |     |
| ------------- | ------ | -------- | --- | ----------- | ------ | ------- | --- | --- | --- | --- | --- | --- |
titudes, along with 2.5D reference maps containing aerial Figure 1. Benchmark Overview. This benchmark focuses on
photogrammetry maps and historical satellite maps. Sec- UAVvisuallocalizationunderlow-altitudemulti-viewconditions
|          |         |           |     |          |              |     | using the 2.5D | aerial | or satellite | reference | maps. | The visual lo- |
| -------- | ------- | --------- | --- | -------- | ------------ | --- | -------------- | ------ | ------------ | --------- | ----- | -------------- |
| ondly, a | unified | framework | was | proposed | to integrate | the |                |        |              |           |       |                |
calizationismainlyachievedviaaunifiedframeworkcombining
| state-of-the-art |     | AVL approaches |     | and comprehensively |     | test |     |     |     |     |     |     |
| ---------------- | --- | -------------- | --- | ------------------- | --- | ---- | --- | --- | --- | --- | --- | --- |
theirperformance. Thebestcombinedmethodwaschosen imageretrieval,imagematching,andPnPproblemsolving.
asthebaselineandthekeyfactorsinfluencinglocalization
| accuracy | are thoroughly |     | analyzed | based | on it. | This base- |     |     |     |     |     |     |
| -------- | -------------- | --- | -------- | ----- | ------ | ---------- | --- | --- | --- | --- | --- | --- |
tion.However,GNSSsignalsarepronetodropoutandjam-
lineachieveda74.1%localizationaccuracywithin5mun-
|     |     |     |     |     |     |     | ming [57], | while INS | suffers | from drifting | over | time [24]. |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --------- | ------- | ------------- | ---- | ---------- |
derlow-altitude,multi-viewconditions.Inaddition,anovel
Consequently,thereisagrowinginterestinvisuallocaliza-
| retrieval | metric | called PDM@K |     | was introduced |     | to better |     |     |     |     |     |     |
| --------- | ------ | ------------ | --- | -------------- | --- | --------- | --- | --- | --- | --- | --- | --- |
tionasatemporaryalternative[7,14,24,25].
| align with | the characteristics |     | of  | the UAV | AVL | task. Over- |     |     |     |     |     |     |
| ---------- | ------------------- | --- | --- | ------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
CurrentUAVvisuallocalizationresearchcanbeprimar-
all,thisbenchmarkrevealedthechallengesoflow-altitude,
multi-view UAV AVL and provided valuable guidance for ily categorized into relative visual localization (RVL) and
|                  |     |             |     |          |     |           | absolute visual      | localization |              | (AVL) [10]. | RVL     | approaches, |
| ---------------- | --- | ----------- | --- | -------- | --- | --------- | -------------------- | ------------ | ------------ | ----------- | ------- | ----------- |
| future research. |     | The dataset |     | and code | are | available | at                   |              |              |             |         |             |
|                  |     |             |     |          |     |           | such as Simultaneous |              | Localization | and         | Mapping | (SLAM)      |
https://github.com/UAV-AVL/Benchmark
|     |     |     |     |     |     |     | [6], are commonly                 |     | used | for short-range | robot           | navigation |
| --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | ---- | --------------- | --------------- | ---------- |
|     |     |     |     |     |     |     | throughframe-to-framematching[7]. |     |      |                 | WhileRVLmethods |            |
donotrequiregeo-taggedmaps,theyalsosufferfromdrift1.
1.Introduction
Incontrast,AVLapproaches,whichinvolvematchingUAV
In recent years, Unmanned Aerial Vehicles (UAVs) have imageswithgeo-taggedreferencemaps, haveinherentim-
been widely used in various fields such as precision agri- munitytodriftandarethefocusofthispaper.
culture,emergencyresponse,andtransportation[12].These Tothebestofourknowledge,mostpreviousstudiesfo-
dronesgenerallyrelyonGlobalNavigationSatelliteSystem cused on nadir-view-based AVL [5, 25, 37, 42, 52]. Be-
| (GNSS) | and inertial | navigation |     | system | (INS) | for localiza- |     |     |     |     |     |     |
| ------ | ------------ | ---------- | --- | ------ | ----- | ------------- | --- | --- | --- | --- | --- | --- |
1NotethatLoopclosurecansomewhatimprovegloballocalizationac-
*Co-firstauthor. curacy,butitishardtoachieveforlong-distanceoutdoorflights[12].
1731

sides, the regions observed for AVL are often assumed as drone-to-satellite retrieval, several studies concentrate on
planar, inwhichtheelevationsaresignificantlylowerthan refining network architectures [31, 43, 50]. For instance,
theUAVflightaltitude[56]. Therefore, onecanuseaffine MCCG [43] incorporates a cross-dimensional interaction
modeltoestimatethetransformationbetweenUAVimages moduleandamulti-classifierstructuretoconstructcompre-
and geo-tagged reference maps [45]. However, as the sig- hensivefeature representations. Additionally, some efforts
nificantviewpointchangesatlowaltitudeintroducesevere arededicatedtoenhancingtrainingandsamplingstrategies
nonlinear transformation between UAV images and refer- [13, 16, 53, 55]. For example, Sample4Geo [16] employs
ence maps, this assumption does not apply to UAV visual InfoNCE loss to increase negative samples for contrastive
localizationunderlow-altitude(< 300m2)andmulti-view learning within one batch. Meanwhile, CAMP [53] intro-
(with pitch angles 3 ranging from 20～ to 90～) conditions. ducescomparisonsbetweendifferentscenesfromthesame
These conditions present greater challenges for visual lo- imaging platform within the same training batch, thereby
calization[58,59]andhowcurrentAVLmethodsperform increasingthenumberofnegativesamplesforcontrast.
in these challenging scenarios is still unclear. Meanwhile, Pixel-Level Image Matching first establishes feature
nopubliclyavailabledatasetscouldbeusedtocomprehen- pointcorrespondencesbetweenUAVimagesandreference
| sively benchmark |     | current | AVL methods. |     | To fill | this gap, |                   |     |         |     |     |         |              |     |
| ---------------- | --- | ------- | ------------ | --- | ------- | --------- | ----------------- | --- | ------- | --- | --- | ------- | ------------ | --- |
|                  |     |         |              |     |         |           | map, subsequently |     | solving | the | PnP | problem | to determine |     |
we constructed a new dataset called AnyVisLoc and con- the UAV＊s location [10, 23]. Pixel-level image matching,
ductedextensiveexperimentsonthisdatasettoevaluateall whichcomprisessparseanddenseapproaches[36],always
UAV AVL methods under low-altitude multi-view condi- achieve higher precision than image-level retrieval. The
tions. Overall,ourcontributionsareasfollows: typical sparse approaches involve keypoint detection and
| ? The first | large-scale |     | low-altitude | multi-view |     | dataset |          |          |        |             |     |          |           |     |
| ----------- | ----------- | --- | ------------ | ---------- | --- | ------- | -------- | -------- | ------ | ----------- | --- | -------- | --------- | --- |
|             |             |     |              |            |     |         | keypoint | matching | steps. | Traditional |     | keypoint | detectors |     |
called AnyVisLoc was proposed. This dataset contains like SIFT [35], SURF [3], and ORB [6] are widely used
18,000 UAV images captured at multiple scenes and al- insparsematchingbutaresensitivetolargeviewpointdif-
titudes,alongwithtwotypesof2.5Dreferencemapsin-
|     |     |     |     |     |     |     | ferences. | The rise | of  | deep learning |     | has brought | learning- |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | -------- | --- | ------------- | --- | ----------- | --------- | --- |
cludingaerialphotogrammetrymapsandsatellitemaps. baseddetectorsanddescriptorsintothemainstreamtocope
? Aunifiedframeworkwasintroducedtointegratethestate-
|     |     |     |     |     |     |     | with viewpoint |     | changes | [15, | 17, | 39, 62]. | Another | line |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ------- | ---- | --- | -------- | ------- | ---- |
of-the-artAVLapproachesandthoroughlytesttheirper- of sparse approaches focuses on learning-based global re-
formance. Thebestcombinedmethodwaschosenasthe lationship modeling among keypoints, such as SuperGlue
baselineandthekeyfactorsinfluencingbaselineaccuracy
|     |     |     |     |     |     |     | [41],Lightglue[32]andOmniglue[28]. |     |     |     |     | Denseapproaches |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- | --- | --- | --------------- | --- | --- |
arethoroughlydiscussed,includingthetypeofreference [18每20,46]avoidkeypointdetectionanddirectlyfinddense
| maps, | different | pitch angles | and | the noise | in  | prior infor- |     |     |     |     |     |     |     |     |
| ----- | --------- | ------------ | --- | --------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
correspondencesbetweenimages,leadingtosignificantim-
| mation. |     |     |     |     |     |     | provementsoversparsemethodsbutwithlowerefficiency. |     |     |     |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- | -------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
? AnovelretrievalmetriccalledPDM@Kwasdesignedto Therefore, thereisgrowinginterestincreatinglightweight
bridgetherelationshipbetweenimageretrievalaccuracy
andhigh-precisionmatchingtechniques[29,36,39,51].
| and final | localization |     | accuracy. | Compared | to  | other met- |            |     |              |     |          |     |            |     |
| --------- | ------------ | --- | --------- | -------- | --- | ---------- | ---------- | --- | ------------ | --- | -------- | --- | ---------- | --- |
|           |              |     |           |          |     |            | UAV Visual |     | Localization |     | Dataset. | As  | summarized | in  |
ricslikeRecall@KandSDM@K,PDM@Kalignsmore
Tab.1,mostcurrentUAVdatasetsfocusonnadir-viewand
closelywiththecharacteristicsoftheUAVAVLtask. lack multi-view coverage [14, 23, 37, 56]. Some datasets
|     |     |     |     |     |     |     | arerestrictedtospecificscenes(e.g., |     |     |     |     | urban[14]orwilder- |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- | ------------------ | --- | --- |
2.RelatedWork
|             |           |     |             |     |          |           | ness [23]  | areas). | Some  | datasets | use    | synthetic | data | (e.g.,   |
| ----------- | --------- | --- | ----------- | --- | -------- | --------- | ---------- | ------- | ----- | -------- | ------ | --------- | ---- | -------- |
|             |           |     |             |     |          |           | Google Map | Studio  | [63]) | that     | do not | fit the   | real | applica- |
| Image-Level | Retrieval |     | can be used | to  | estimate | the rough |            |         |       |          |        |           |      |          |
positionofUAVimageonthereferencemap[8,58]. These tion requirement. Although some recent geo-localization
|     |     |     |     |     |     |     | datasetsincludemulti-viewUAVimages[63,65], |     |     |     |     |     |     | theyof- |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- | --- | ------- |
approachesincludesTemplateMatching(TM)[48]andVi-
sualGeo-localization(VG)[4]methods. Allthesemethods tenlackgroundtruthforUAVpositionsandcontinuousge-
ographicalcoverage,whichisnotsuitableforpreciseAVL.
| rely on constructing |     | feature | patterns | to  | measure | similarity |     |     |     |     |     |     |     |     |
| -------------------- | --- | ------- | -------- | --- | ------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
betweendrone(query)andreference(gallery)images. The Regardingreferencemaps, mostdatasetscurrentlyonly
similaritymetricscommonlyusedforTM(e.g.,NCC[48], have 2D satellite images and lack high-precision digital
MI [60]) are not invariant to viewpoint differences, mak- surface model (DSM) [56]. Open-source products such
ing them less suitable for low-altitude, multi-view condi- as ALOS DSM 30m [38] and NASADEM 30m [30] have
|           |           |      |                |     |            |     | relatively | low spatial | resolutions |     | and | do not | meet | the pre- |
| --------- | --------- | ---- | -------------- | --- | ---------- | --- | ---------- | ----------- | ----------- | --- | --- | ------ | ---- | -------- |
| tions. In | contrast, | deep | learning-based |     | VG methods | are |            |             |             |     |     |        |      |          |
more adaptable to changes in viewpoint [65]. NetVLAD ciseAVLrequirementsunderlow-altitudemulti-viewcon-
| [2] is a | widely | adopted | VG baseline. |     | In the | field of | ditions. |      |        |            |     |         |     |          |
| -------- | ------ | ------- | ------------ | --- | ------ | -------- | -------- | ---- | ------ | ---------- | --- | ------- | --- | -------- |
|          |        |         |              |     |        |          | To the   | best | of our | knowledge, |     | none of | the | existing |
2Accordingtorelevantregulations,civilianUAVsarenotpermittedto
|     |     |     |     |     |     |     | datasets | simultaneously |     | provide | aerial | reference | map | and |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------------- | --- | ------- | ------ | --------- | --- | --- |
flyabove300meters[1]
3theanglebetweentheopticalaxisandthehorizontalplane satellite reference map of the same area. The works most
1732

Table1.UAVAVLDatasetsComparison
Name Year UAVdata UAVTypes UAVLocation 2DReference DSM FlightAltitude Observation Scenes Temporal
|     |     |     |     |     |     | (cid:2) | ℅   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
ATM[37] 2021 Real-scenes 1 Aerial unknown Nadir-view Urban Multiple
University-1652[63] 2021 Synthetic - ℅ Satellite ℅ 121.5mto256m Multi-view Buildings -
|     |     |     |     |     |     | (cid:2) | ℅   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
Wildnav[23] 2022 Synthetic - Satellite unknown Nadir-view Wilderness -
VPAIR[42] 2022 Real-scenes 1 (cid:2) Satellite (cid:2) 300mto400m Nadir-view Multiple -
SEUS-200[65] 2023 Real-scenes - ℅ Satellite ℅ 150/200/250/300m Multi-view Urban -
|     |     |     |     |     |     | (cid:2) | ℅   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
DenseUAV[14] 2024 Real-scenes 1 Satellite 80m/90m/100m Nadir-view Urban Multiple
UAVD4L[54] 2024 Real-scenes 1 (cid:2) Aerial (cid:2) 50mto151m Multi-view Urban -
UAV-VisLoc[56] 2024 Real-scenes unknown (cid:2) Satellite ℅ 400mto2000m Nadir-view Multiple Multiple
|     |     |     |     |     |     | (cid:2) | ℅   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
GTA-UAV[27] 2025 Synthetic - Satellite 80mto650m Nearnadir-view Multiple -
CVGL-RGBT[64] 2025 Real-scenes 1 ℅ Satellite ℅ unknown Multi-view Multiple Multiple
AnyVisLoc(Ours) 2026 Real-scenes 7 (cid:2) Aerial&Satellite (cid:2) 30mto300m Multi-view Multiple Multiple
similartooursare[10,45,49,58],althoughtheseliterature retrievalandmatchingmodelsspecificallytailoredforUAV
exploredthefeasibilityofAVLbasedonoblique-view,their AVLtasks. Thecorrespondenceestablishmentprocessand
test data lacked sufficient scene coverage, and the datasets ourtrainingresultsaredetailedintheappendix.
andcodeswerenotopen-sourcedyet.
(cid:51)(cid:51)(cid:76)(cid:76)(cid:87)(cid:87)(cid:70)(cid:70)(cid:75)(cid:75)(cid:36)(cid:36)(cid:81)(cid:81)(cid:74)(cid:74)(cid:79)(cid:79)(cid:72)(cid:72)
3.AnyVisLocDataset (cid:41)(cid:79)(cid:76)(cid:74)(cid:75)(cid:87)(cid:36)(cid:79)(cid:87)(cid:76)(cid:87)(cid:88)(cid:71)(cid:72) (cid:51)(cid:76)(cid:87)(cid:70)(cid:75)(cid:36)(cid:81)(cid:74)(cid:79)(cid:72)
| The accuracy    | of                 | UAV         | AVL is     | affected           | by     | various fac- |     |     |     |     |     |     |     |     |
| --------------- | ------------------ | ----------- | ---------- | ------------------ | ------ | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
| tors including  | observation        |             | conditions | (e.g.,             | flight | altitude,    |     |     |     |     |     |     |     |     |
| pitch angle,    | and                | field of    | view),     | flight environment |        | (scene,      |     |     |     |     |     |     |     |     |
| weather,        | and illumination), |             | and        | reference          | map    | character-   |     |     |     |     |     |     |     |     |
| istics (source, | spatial            | resolution, |            | and modality       |        | differences) |     |     |     |     |     |     |     |     |
| [12, 58].       | Our proposed       |             | AnyVisLoc  | dataset            | covers | all pos-     |     |     |     |     |     |     |     |     |
sible factors for UAV AVL under low-altitude multi-view Figure2.FlightAltitudeandPitchAngleDistribution.
observationcondition.Thissectiongivesadetaileddescrip-
tionofit.
3.2.DataCharacteristics
3.1.DataAcquisitionandProcessing
|     |     |     |     |     |     |     | ? Multi-altitude: |     | Our | dataset | covers | low-altitude |     | flight |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | ------- | ------ | ------------ | --- | ------ |
We collected a total of 18,000 UAV images using seven conditionsfrom30mto300m(seeFig.2andFig.3).
differenttypesofDJIdrones4, whosecamerashavediffer- ? Multi-view: Our dataset covers pitch angle from 20～ to
90～(seeFig.2andFig.3).
| ent intrinsic | parameters. |     | As shown | in  | Fig. 3, | the images |     |     |     |     |     |     |     |     |
| ------------- | ----------- | --- | -------- | --- | ------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
weretakenin15citiesacrossChinaunderdifferentweather ? Multi-scene: Our dataset includes various scenes (see
Fig.3),suchasdenseurbanareas(e.g.,citiesandtowns),
(sunny,cloudy,rainy),seasons,andilluminations(dayand
night),covering25distinctregions. Theimagingcoverage typical landmark scenes (e.g., playground, museums,
arearangesfrom10,000m2 to9,000,000m2. Eachimage church), natural scenes (e.g., farmland and mountains),
andmixedscenes(e.g.,universitiesandparks).
| is attached | with | camera | intrinsic | and extrinsic |     | parameters, |     |     |     |     |     |     |     |     |
| ----------- | ---- | ------ | --------- | ------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
whichcanbeusedforUAVAVLaswellasthegroundtruth. ? Multi-referencemap: Ourdatasetprovidestwotypesof
|          |           |             |                |       |         |             | 2.5D reference |     | maps | for different |            | purposes | (see | Fig. 3). |
| -------- | --------- | ----------- | -------------- | ----- | ------- | ----------- | -------------- | --- | ---- | ------------- | ---------- | -------- | ---- | -------- |
| Besides  | the       | UAV images, | two            | types | of 2.5D | reference   |                |     |      |               |            |          |      |          |
|          |           |             |                |       |         |             | The aerial     | map | with | high spatial  | resolution |          | can  | be used  |
| maps are | provided: | Aerial      | Photogrammetry |       |         | Map that is |                |     |      |               |            |          |      |          |
createdbycapturingimagesusingtheDJIdronesandthen for high-precision localization but requires prior aerial
|     |     |     |     |     |     |     | photogrammetry. |     | The | satellite | map | serves | as an | alterna- |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --- | --------- | --- | ------ | ----- | -------- |
applyingmodernStructure-from-Motiontechniques[54]to
construct2DorthomosaicandDSM.SatelliteMapthatin- tivewhentheaerialmapisunavailable.
Overall,ourdatasetcanfacilitateacomprehensiveeval-
volves2DhistoricalimagesfromGoogleEarthandALOS
|     |     |     |     |     |     |     | uation | of current | UAV | AVL | methods | under | low-altitude |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | ---------- | --- | --- | ------- | ----- | ------------ | --- |
30mDSM.Bothsetsof2.5Dreferencemapsaregeo-tagged
and reprojected into the UTM coordinate system for geo- multi-viewobservationconditions.
localization.
4.TheUnifiedAVLFramework
Beyondtheseresources,wealsoprovidehigh-precision
| correspondences |      | between  | UAV | images    | and the | aerial pho- |                  |           |                |         |          |               |      |           |
| --------------- | ---- | -------- | --- | --------- | ------- | ----------- | ---------------- | --------- | -------------- | ------- | -------- | ------------- | ---- | --------- |
|                 |      |          |     |           |         |             | Given a          | UAV       | image captured |         | under    | low-altitude, |      | multi-    |
| togrammetry     | map, | enabling | the | community | to      | train image |                  |           |                |         |          |               |      |           |
|                 |      |          |     |           |         |             | view conditions, |           | its field      | of view | is       | within        | the  | reference |
|                 |      |          |     |           |         |             | map, but         | its exact | position       | is      | unknown. | Under         | such | con-      |
4Mavic2,Mavic3,Mavic3Pro,Phantom3,Phantom4,Phantom4
RTK,Mini4Pro ditions,extremeviewpointchangesandavastsearchspace
1733

(cid:51)(cid:79)(cid:68)(cid:92)(cid:74)(cid:85)(cid:82)(cid:88)(cid:81)(cid:71)(cid:3)(cid:3)(cid:22)(cid:19)(cid:19)(cid:80)(cid:3)(cid:3)(cid:28)(cid:19)～ (cid:38)(cid:82)(cid:88)(cid:81)(cid:87)(cid:85)(cid:92)(cid:3)(cid:3)(cid:21)(cid:19)(cid:21)(cid:80)(cid:3)(cid:3)(cid:26)(cid:19)～ (cid:48)(cid:82)(cid:88)(cid:81)(cid:87)(cid:68)(cid:76)(cid:81)(cid:3)(cid:3)(cid:22)(cid:19)(cid:19)(cid:80)(cid:3)(cid:3)(cid:25)(cid:19)～ (cid:41)(cid:68)(cid:85)(cid:80)(cid:79)(cid:68)(cid:81)(cid:71)(cid:3)(cid:3)(cid:21)(cid:24)(cid:19)(cid:80)(cid:3)(cid:3)(cid:25)(cid:19)～ (cid:41)(cid:76)(cid:79)(cid:80)(cid:3)(cid:55)(cid:82)(cid:90)(cid:81)(cid:3)(cid:3)(cid:20)(cid:22)(cid:26)(cid:80)(cid:3)(cid:3)(cid:24)(cid:26)～ (cid:38)(cid:76)(cid:87)(cid:92)(cid:3)(cid:3)(cid:21)(cid:19)(cid:19)(cid:80)(cid:3)(cid:3)(cid:23)(cid:26)～
(cid:51)(cid:68)(cid:85)(cid:78)(cid:3)(cid:3)(cid:20)(cid:20)(cid:26)(cid:80)(cid:3)(cid:3)(cid:23)(cid:24)～ (cid:56)(cid:81)(cid:76)(cid:89)(cid:72)(cid:85)(cid:86)(cid:76)(cid:87)(cid:92)(cid:3)(cid:3)(cid:26)(cid:25)(cid:80)(cid:3)(cid:3)(cid:23)(cid:21)～ (cid:48)(cid:88)(cid:86)(cid:72)(cid:88)(cid:80)(cid:20)(cid:3)(cid:28)(cid:28)(cid:80)(cid:3)(cid:3)(cid:23)(cid:24)～ (cid:48)(cid:88)(cid:86)(cid:72)(cid:88)(cid:80)(cid:21)(cid:3)(cid:24)(cid:19)(cid:80)(cid:3)(cid:3)(cid:22)(cid:24)～ (cid:48)(cid:88)(cid:86)(cid:72)(cid:88)(cid:80)(cid:22)(cid:3)(cid:20)(cid:19)(cid:19)(cid:80)(cid:3)(cid:3)(cid:22)(cid:24)～ (cid:38)(cid:75)(cid:88)(cid:85)(cid:70)(cid:75)(cid:3)(cid:3)(cid:20)(cid:23)(cid:25)(cid:80)(cid:3)(cid:3)(cid:22)(cid:20)～
(cid:36)(cid:72)(cid:85)(cid:76)(cid:68)(cid:79)(cid:3)(cid:53)(cid:72)(cid:73)(cid:72)(cid:85)(cid:72)(cid:81)(cid:70)(cid:72)(cid:3)(cid:48)(cid:68)(cid:83)(cid:3)(cid:11)(cid:19)(cid:17)(cid:19)(cid:21)(cid:80)(cid:3)(cid:97)(cid:3)(cid:19)(cid:17)(cid:22)(cid:24)(cid:80)(cid:12) (cid:36)(cid:72)(cid:85)(cid:76)(cid:68)(cid:79)(cid:3)(cid:3)(cid:51)(cid:75)(cid:82)(cid:87)(cid:82)(cid:74)(cid:85)(cid:68)(cid:80)(cid:80)(cid:72)(cid:87)(cid:85)(cid:92)(cid:3)(cid:39)(cid:54)(cid:48)(cid:3)(cid:11)ˉ(cid:21)(cid:17)(cid:24)(cid:80)(cid:12) (cid:54)(cid:68)(cid:87)(cid:72)(cid:79)(cid:79)(cid:76)(cid:87)(cid:72)(cid:3)(cid:53)(cid:72)(cid:73)(cid:72)(cid:85)(cid:72)(cid:81)(cid:70)(cid:72)(cid:3)(cid:48)(cid:68)(cid:83)(cid:3)(cid:11)(cid:19)(cid:17)(cid:20)(cid:22)(cid:80)(cid:3)(cid:97)(cid:3)(cid:19)(cid:17)(cid:24)(cid:24)(cid:80)(cid:12) (cid:36)(cid:47)(cid:50)(cid:54)(cid:3)(cid:22)(cid:19)(cid:80)(cid:3)(cid:39)(cid:54)(cid:48)
Figure3. DatasetOverview. TheAnyVisLocdatasetcontainsmulti-scene,multi-altitude,andmulti-viewUAVimagestakenin15cities
acrossChina,aswellasaerialandsatellitereferencemaps.EachUAVimageshowsitsflightaltitudeandpitchanglebelow.
always result in image matching failures. Meanwhile, im- UAVimageandthereferencemapwithoutretrieval[61].
age retrieval can only provide a rough estimate of the cur- Localization Metric: The localization accuracy is de-
rentview＊sposition. Consequently,independentlyevaluat- notedasA@T = NT ℅100%,whichmeansthecorrectlocal-
|     |     |     |     |     |     | N   |     | T   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ing the performance of image retrieval or matching meth- ization ratio under a given threshold of meters. The lo-
(cid:2)
ods becomes challenging. Therefore, a unified framework calization error is denoted as e = (x ?x )2+(y ?y )2,
|     |     |     |     |     |       |         | i   | p g p | g   |
| --- | --- | --- | --- | --- | ----- | ------- | --- | ----- | --- |
|     |     |     |     |     | (x ,y | ) (x ,y | )   |       |     |
isneededforfairandmeaningfultesting. where p p and g g are the UTM coordinates of
predictedlocationandthegroundtruth,respectively.
| FrameworkWorkflow: |     | AsshowninFig.1,theframe- |     |     |     |     |     |     |     |
| ------------------ | --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- |
work operates in a coarse-to-fine manner. Initially, image- Retrieval Metric: The Recall@K and our proposed
|                 |            |                             |           | PixelDistanceMetric(PDM@K,seeEq.(1))areused. |                                             |           |             |     | In  |
| --------------- | ---------- | --------------------------- | --------- | -------------------------------------------- | ------------------------------------------- | --------- | ----------- | --- | --- |
| level retrieval | is used to | estimate the rough position | of the    |                                              |                                             |           |             |     |     |
|                 |            |                             |           | Eq.(1),                                      | R denotestheoverlapratebetweenretrievalsand |           |             |     |     |
| current view,   | followed   | by pixel-level matching     | to obtain |                                              | i                                           |           |             |     |     |
|                 |            |                             |           |                                              |                                             | R = d /(w | ﹞r), whered |     |     |
2D-2D matched point pairs between the UAV image and thegroundtruth, i i i i isthespatial
|                  |                                  |     |     | distance, | w isthewidthofthegalleryimage, |     |     | andr | isthe |
| ---------------- | -------------------------------- | --- | --- | --------- | ------------------------------ | --- | --- | ---- | ----- |
| thereferencemap. | Subsequently,DSMdataandthematch- |     |     |           | i                              |     |     |      |       |
e?竹﹞(Ri?汐)
ingresultsareusedtosolvethePnPproblemanddetermine spatialresolutionofthereferencemap. isthe
1+e?竹﹞(Ri?汐)
theUAV＊sgeo-location. Thisframeworkcanintegratewith retrievalscoreofthei-thsampleintheretrievalresultorder
|     |     |     |     | and(K | ?i+1)istheweight. |     | 竹and汐areweightfactors. |     |     |
| --- | --- | --- | --- | ----- | ----------------- | --- | ---------------------- | --- | --- |
differentreferencemapsandlocalizationstrategies.
|     |     |     |     | Inthispaper,竹issetto6and汐issetto0.9. |     |     |     | Alargervalue |     |
| --- | --- | --- | --- | ------------------------------------ | --- | --- | --- | ------------ | --- |
IntegratedAlgorithms:Theimageretrievalapproaches
include template matching approaches like NCC [48] and of PDM@K indicates a better retrieval performance. The
rationaleofthismetricisdetailedinSec.5.2.
| MI [60], | popular retrieval | models like NetVLAD | [2], and |     |     |     |     |     |     |
| -------- | ----------------- | ------------------- | -------- | --- | --- | --- | --- | --- | --- |
d r o n e - to - s a te l li te r e tr ie v a l a p p r o a ch e s s u c h a s C N N -b as e d (cid:3)K (cid:3)K
(K?i+1)﹞e?竹﹞(Ri?汐)/
|     |     |     |     | PDM@K | =   |     |     | (K?i+1). | (1) |
| --- | --- | --- | --- | ----- | --- | --- | --- | -------- | --- |
m o d e l s [ 1 1 , 1 6 , 21 , 3 1 , 4 3 , 5 0 ] a n d tr a n s fo r m e r- ba s ed m o d - 1+e?竹﹞(Ri?汐)
|                                        |     |                                |           |                |     | i=1      |                 | i=1  |      |
| -------------------------------------- | --- | ------------------------------ | --------- | -------------- | --- | -------- | --------------- | ---- | ---- |
| els[13,14,26,53,55].                   |     | Matchingtechniquesincludehand- |           |                |     |          |                 |      |      |
| craftedmethodssuchasSIFT[35]andORB[6], |     |                                | learning- |                |     |          |                 |      |      |
|                                        |     |                                |           | Implementation |     | Details: | Our experiments | were | con- |
basedsparsefeatureapproaches[15,17,28,29,32,33,39,
|                  |       |                            |          | ducted | on a machine | equipped   | with | Intel Core i9-10920X |      |
| ---------------- | ----- | -------------------------- | -------- | ------ | ------------ | ---------- | ---- | -------------------- | ---- |
| 41, 62], (semi-) | dense | feature approaches [18每20, | 46, 47], |        |              |            |      |                      |      |
|                  |       |                            |          | CPU    | @ 3.50GHz    | (128G RAM) | and  | NVIDIA RTX           | 3090 |
along with large-scale training frameworks [40, 44]. The GPU(24G). For deep learning-based image retrieval ap-
PnPsolverisP3P+RANSAC[22].
proaches,weusetheweighttrainedontheUniversity-1652
Additionally, we compare four localization strategies: dataset [63] with an image size of 384 ℅ 384. For deep
(a)MatchingtheTop-1retrievalimage[58],(b)Re-ranking learning-based image matching approaches, we adopted
Top-K retrievals based on the number of inliers [9], (c) weightsandinputsizesfromexistingworkstoleveragethe
Matching all gallery images followed by most inliers sort- models＊optimalperformancewhiletestingtheirgeneraliza-
ing[23],(d)Directlyperformspixelmatchingbetweenthe tion capabilities. For NCCand MI,we employedour own
1734

implementations. ForSIFT,ORBandPnPsolver,weused RoMa)anddifferentlocalizationstrategies(Top1Matching
OpenCVimplementations. Notably,weusetheUAV＊salti- andTop5Re-rankbasedonthenumberofinliers).
tudeandpitch/yawinformationtoroughlyestimatetheim- From Tab. 3, we can observe that CAMP achieves the
age＊s scale and rotation, which helps to narrow the search highest localization accuracy. This is consistent with the
space. FurtherdiscussiononthissetupisinSec.6.3. trendobservedinTab.2.
5.2.ImageRetrievalMetric
5.ExperimentsonAVLFramework
InUAVAVLtasks,referencemapsaregeographicallycon-
BasedontheunifiedAVLframework,weevaluatestate-of- tinuous, yet Recall@K solely focuses on the result with
| the-art image | retrieval    | and        | matching approaches |           | alongside |                      |     |        |              |     |              |     |
| ------------- | ------------ | ---------- | ------------------- | --------- | --------- | -------------------- | --- | ------ | ------------ | --- | ------------ | --- |
|               |              |            |                     |           |           | minimal localization |     | error, | disregarding | the | distribution | of  |
| different     | localization | strategies | in Sec.             | 5.1, Sec. | 5.3, and  |                      |     |        |              |     |              |     |
otherimageswithinTopK.AsshowninFig.4a,Recall@1
Sec.5.4,respectively. Theseexperimentsareconductedus- assigns a binary score (1 or 0) to retrieval results, which
| ing a subset | of UAV | images | and the aerial | map. | The best |                                                      |     |     |     |     |     |     |
| ------------ | ------ | ------ | -------------- | ---- | -------- | ---------------------------------------------------- | --- | --- | --- | --- | --- | --- |
|              |        |        |                |      |          | failstoaccountforthespatialdistributionofretrievals. |     |     |     |     |     | For |
combinedmethodisthenselectedasthebaselineandevalu- instance,inFig.5,the4thrankedimage,despiteitsdistance
| atedonthecompletedatasetinSec.5.5. |     |     |     | Wefurtherpresent |     |                 |     |                    |     |         |         |       |
| ---------------------------------- | --- | --- | --- | ---------------- | --- | --------------- | --- | ------------------ | --- | ------- | ------- | ----- |
|                                    |     |     |     |                  |     | from the ground |     | truth, effectively |     | matches | the UAV | image |
ananalysisofourproposedPDM@KmetricinSec.5.2.
|     |     |     |     |     |     | withalocalizationerrorof3.8m. |     |     |     | Therefore,itisunreason- |     |     |
| --- | --- | --- | --- | --- | --- | ----------------------------- | --- | --- | --- | ----------------------- | --- | --- |
ableforRecall@Ktoassignthisresultascoreof0.
5.1.ImageretrievalApproach
TheSpatialDistanceMetric[14](SDM@K,seeEq.(2))
partiallyaddressesthisissuebyconsideringthespatialdis-
|     |     |     |     |     |     | tribution of | retrieval | results. | However, | SDM@K |     | relies on |
| --- | --- | --- | --- | --- | --- | ------------ | --------- | -------- | -------- | ----- | --- | --------- |
Table2.PerformanceMetricsofRetrievalApproaches
d
|     |     |     |     |     |     | the spatial | distance | between | the | ground | truth | and the |
| --- | --- | --- | --- | --- | --- | ----------- | -------- | ------- | --- | ------ | ----- | ------- |
i
Method R@1 R@3 R@5 P@1 P@3 P@5 ms/feat closest retrievals, making it sensitive to variations in the
| NCC[48] |     | 0.3 1.5 | 2.6 0.193 | 0.189 | 0.189 17? |                                   |     |     |     |                      |     |     |
| ------- | --- | ------- | --------- | ----- | --------- | --------------------------------- | --- | --- | --- | -------------------- | --- | --- |
|         |     |         |           |       | 20?       | spatialresolutionofreferencemaps. |     |     |     | Thisleadstoinconsis- |     |     |
| MI[60]  |     | 2.4 5.9 | 8.6 0.352 | 0.333 | 0.323     |                                   |     |     |     |                      |     |     |
tentscorecurvesacrossdifferentmaps(seeFig.4a),which
| NetVLAD[2] | 31.1 | 53.9 | 64.9 0.741 | 0.695 | 0.652 11 |     |     |     |     |     |     |     |
| ---------- | ---- | ---- | ---------- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
isunfairforevaluation.
| LPN[50]    | 41.1 | 62.1 | 70.4 0.799 | 0.719 | 0.665 5 |     |     |     |     |     |     |     |
| ---------- | ---- | ---- | ---------- | ----- | ------- | --- | --- | --- | --- | --- | --- | --- |
| RK-Net[31] | 45.3 | 67.8 | 76.1 0.848 | 0.775 | 0.712 9 |     |     |     |     |     |     |     |
F S R A [1 3 ] 5 2 . 9 7 3 . 9 8 1 . 2 0 . 8 7 0 0 . 7 8 0 0 . 7 1 7 5 (cid:3)K (cid:3)K
|     |     |     |     |     |     | SDM@K |     | = (K | ? i + 1)/ | (K  | ?i+1). |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | ---- | --------- | --- | ------ | --- |
D e ns eU A V [14] 5 1 . 6 6 9 . 4 7 6 . 7 0 . 8 5 4 0 . 7 5 4 0 . 6 8 4 6 (2)
e s﹞ d i
| MEAN[11] | 48.0 | 70.8 | 77.1 0.846 | 0.752 | 0.684 4 |     |     | i=1 |     | i=1 |     |     |
| -------- | ---- | ---- | ---------- | ----- | ------- | --- | --- | --- | --- | --- | --- | --- |
| LRFR[21] | 53.4 | 73.0 | 80.6 0.852 | 0.750 | 0.683 4 |     |     |     |     |     |     |     |
QDFL[26] 56.5 79.8 86.7 0.906 0.825 0.759 20 Incontrast,PDM@Knormalizesboththeimagesizeand
| DAC[55] | 58.3 | 78.6 | 84.4 0.899 | 0.808 | 0.733 8 |     |     | R   | = d /(w | ﹞ r), |     |     |
| ------- | ---- | ---- | ---------- | ----- | ------- | --- | --- | --- | ------- | ----- | --- | --- |
MCCG[43] 56.7 80.5 88.6 0.901 0.841 0.779 6 spatial resolution with i i i ensuring a fair
Sample4Geo[16] 58.6 79.9 86.4 0.907 0.825 0.760 13 evaluationacrossdiverseregions＊referencemaps.
CAMP[53] 62.4 82.7 88.3 0.920 0.834 0.766 6 Moreover, PDM@K effectively bridges image retrieval
|     |     |     |     |     |     | accuracy with | final | localization | accuracy. |     | As illustrated | in  |
| --- | --- | --- | --- | --- | --- | ------------- | ----- | ------------ | --------- | --- | -------------- | --- |
This section aims to identify the best retrieval ap- Fig. 5, R is correlated with the distance between the re-
i
| proaches. | As shown | in  | Tab. 2, the handcrafted |     | template |     |     |     |     |     |     |     |
| --------- | -------- | --- | ----------------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
trievedpositionandgroundtruth,reflectingtheoverlaprate
matching approaches, NCC and MI, perform worst since ofimagepairsforsubsequentimagematching-basedlocal-
theyaresensitivetoviewpointdifference. ization. Higher R indicates lower overlap, increasing im-
i
Among deep learning methods, models like CAMP, agematchingdifficultyandreducinglocalizationaccuracy.
Sample4Geo,DAC,andMCCGwhichuseConvNeXt[34] For example, in Fig. 5, the first retrieval with R = 0.27
i
| as the backbone | achieved |     | better performance: |     | MCCG op- |             |       |          |       |            |           |      |
| --------------- | -------- | --- | ------------------- | --- | -------- | ----------- | ----- | -------- | ----- | ---------- | --------- | ---- |
|                 |          |     |                     |     |          | achieves an | error | of 1.4m, | while | the second | retrieval | with |
timizes network structure for better feature representation, R = 0.35 has an error of 2.1m. In contrast, the third re-
i
whileSample4Geo,DACandCAMPfocusontheimprove- trieval with R = 1.37 leads to localization failure, with
i
| mentsoftrainingandsamplestrategies, |     |     |     | whichrevealsthat |     |             |      |                     |     |          |      |          |
| ----------------------------------- | --- | --- | --- | ---------------- | --- | ----------- | ---- | ------------------- | --- | -------- | ---- | -------- |
|                                     |     |     |     |                  |     | an error of | 649m | due to insufficient |     | overlap. | This | trend is |
training and sampling strategies are more effective for im- furthersupportedbytheexperimentallocalizationaccuracy
provingtheaccuracyofcurrentimageretrievalmodels.
distributionpresentedinFig.4c.
|     |     |     |     |     |     |     |     |     |     | f(R ) |     | 汐   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
AlthoughDenseUAVproposedanewbaselineforAVL, For the retrieval score function (see Fig. 4b),
i
it underperformed in multi-view conditions, possibly be- determinestheR thresholdatwhichthescoredrops,while
i
|     |     |     |     |     |     | 竹controlsthesharpnessofthedecay. |     |     |     | WhenR |     |     |
| --- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | ----- | --- | --- |
cause the model was mainly designed for nadir-view im- i exceedsthe
ages. Overall,drone-to-orthoreferencemapretrievalunder normalized diagonal length of the image, l (e.g., l = 1.67
low-altitude,multi-viewconditionsisstillchallenging.
|     |     |     |     |     |     | when the | aspect | ratio of drone | image | is  | 4:3), there | is no |
| --- | --- | --- | --- | --- | --- | -------- | ------ | -------------- | ----- | --- | ----------- | ----- |
Toanalyzetheimpactofretrievalaccuracyonthesubse- overlapbetweentheimages,resultinginascoreof0.There-
quentlocalizationaccuracy,wealsocombinedretrievalap- fore, 汐 should be set slightly above l/2, and 竹 can be ad-
proaches with different matching approaches (SP+LG and justed based on the impact of different overlap rates on
1735

Table3.LocalizationResultsofDifferentImageRetrievalApproaches.
| Method |     |     | Top1+SPLG |     | Top1+RoMa |     |     | Top5Re-rank+SPLG |     |     |     | Top5Re-rank+RoMa |     |     |
| ------ | --- | --- | --------- | --- | --------- | --- | --- | ---------------- | --- | --- | --- | ---------------- | --- | --- |
A@5m A@10m A@20m A@5m A@10m A@20m A@5m A@10m A@20m A@5m A@10m A@20m
NCC[48] 7.5 9.8 11.4 10.8 13.3 15.2 16.5 22.1 26.2 22.4 28.3 31.4
MI[60] 13.6 18.6 21.4 18.3 21.7 25.4 28.9 38.8 45.0 36.4 44.6 49.7
NetVLAD[2] 41.7 55.3 62.8 49.3 60.0 65.1 55.0 72.1 80.7 64.3 76.6 82.9
LPN[50] 43.6 57.3 66.5 54.1 64.2 69.5 57.1 75.0 84.6 66.8 80.5 86.4
RK-Net[31] 49.9 66.6 76.2 62.2 73.9 79.4 60.0 77.5 87.2 68.6 82.6 89.1
FSRA[13] 51.6 69.3 79.4 64.9 76.7 82.2 60.7 80.5 90.4 71.7 84.9 91.7
DenseUAV[14] 49.7 66.5 76.4 61.7 72.9 79.8 59.0 78.2 88.1 70.3 84.2 90.6
MEAN[11] 48.8 65.4 72.9 59.8 70.6 76.8 59.0 79.3 88.1 70.2 84.1 90.6
LRFR[21] 51.6 68.8 77.2 63.1 73.4 79.9 60.0 79.5 88.6 71.4 84.8 91.5
QDFL[26] 55.1 74.4 82.7 67.5 79.4 85.8 62.4 81.5 91.1 73.0 86.2 93.0
DAC[55] 53.4 71.3 81.7 66.9 78.8 85.1 62.2 81.8 91.6 72.7 86.9 93.0
MCCG[43] 54.9 74.2 83.6 68.2 81.4 87.4 63.1 82.1 91.9 72.7 86.2 92.8
Sample4Geo[16] 54.1 72.8 83.2 66.9 78.8 85.7 62.4 82.4 91.9 73.2 87.5 93.7
CAMP[53] 55.8 75.0 85.1 70.1 81.3 87.6 62.4 82.2 92.4 74.6 87.6 94.2
(cid:20)(cid:17)(cid:19) (cid:51)(cid:39)(cid:48)(cid:35)(cid:20) (cid:20)(cid:17)(cid:19) (cid:20)(cid:17)(cid:19)
?(cid:3404)?.??(cid:3404)?
(cid:72)(cid:85)(cid:82)(cid:70)(cid:54) (cid:53)(cid:72)(cid:70)(cid:68)(cid:79)(cid:79)(cid:35)(cid:20) ?(cid:3404)?.??(cid:3404)? (cid:17)(cid:70)(cid:70)(cid:36)
|     |     |     | (cid:54)(cid:39)(cid:48)(cid:35)(cid:20)(cid:54)(cid:53)(cid:29)(cid:19)(cid:17)(cid:19)(cid:21)(cid:80) | (cid:72)(cid:85)(cid:82)(cid:70)(cid:54) |     |     | ?(cid:3404)?.??(cid:3404)? |     |     |     |     |     |     |     |
| --- | --- | --- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------- | --- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- |
(cid:36)(cid:35)(cid:21)(cid:19)(cid:80)
|     |     |     | (cid:54)(cid:39)(cid:48)(cid:35)(cid:20)(cid:54)(cid:53)(cid:29)(cid:19)(cid:17)(cid:19)(cid:23)(cid:80) |     |     |     | ?(cid:3404)?.??(cid:3404)? |     | (cid:81)(cid:82)(cid:76)(cid:87)(cid:68)(cid:93)(cid:76)(cid:79)(cid:68)(cid:70)(cid:82)(cid:47) |     |     |     |     |     |
| --- | --- | --- | -------------------------------------------------------------------------------------------------------- | --- | --- | --- | -------------------------- | --- | ------------------------------------------------------------------------------------------------ | --- | --- | --- | --- | --- |
(cid:54)(cid:39)(cid:48)(cid:35)(cid:20)(cid:54)(cid:53)(cid:29)(cid:19)(cid:17)(cid:19)(cid:24)(cid:80) ?(cid:3404)?.??(cid:3404)? (cid:36)(cid:35)(cid:20)(cid:19)(cid:80)
(cid:79)(cid:68)(cid:89)(cid:72)(cid:76)(cid:85)(cid:87)(cid:72)(cid:53) (cid:19)(cid:17)(cid:24) (cid:79)(cid:68)(cid:89)(cid:72)(cid:76)(cid:85)(cid:87)(cid:72)(cid:53) (cid:19)(cid:17)(cid:24) (cid:19)(cid:17)(cid:24) (cid:36)(cid:35)(cid:24)(cid:80)
|     |     |     |     |     | ?(cid:4666)? (cid:4667) |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
?
?(cid:2879)?(cid:4666)??(cid:2879)?(cid:4667)
(cid:3404)
?(cid:3397)?(cid:2879)?(cid:4666)??(cid:2879)?(cid:4667)
| (cid:19) | (cid:19)(cid:17)(cid:24) |     | (cid:20)(cid:17)(cid:19) (cid:20)(cid:17)(cid:24) | (cid:19) |                          |                          |     | (cid:20)(cid:17)(cid:24) |     |          |                          |                          |     |                          |
| -------- | ------------------------ | --- | ------------------------------------------------- | -------- | ------------------------ | ------------------------ | --- | ------------------------ | --- | -------- | ------------------------ | ------------------------ | --- | ------------------------ |
|          |                          |     |                                                   |          | (cid:19)(cid:17)(cid:24) | (cid:20)(cid:17)(cid:19) |     |                          |     | (cid:19) | (cid:19)(cid:17)(cid:24) | (cid:20)(cid:17)(cid:19) |     | (cid:20)(cid:17)(cid:24) |
|          |                          | ?   |                                                   |          |                          | ?                        |     |                          |     |          |                          | ?                        |     |                          |
|          |                          | ?   |                                                   |          |                          | ?                        |     |                          |     |          |                          |                          | ?   |                          |
(cid:11)(cid:68)(cid:12)(cid:39)(cid:76)(cid:73)(cid:73)(cid:72)(cid:85)(cid:72)(cid:81)(cid:87)(cid:53)(cid:72)(cid:87)(cid:85)(cid:76)(cid:72)(cid:89)(cid:68)(cid:79)(cid:48)(cid:72)(cid:87)(cid:85)(cid:76)(cid:70)(cid:86) (cid:11)(cid:69)(cid:12)(cid:39)(cid:76)(cid:73)(cid:73)(cid:72)(cid:85)(cid:72)(cid:81)(cid:87)(cid:51)(cid:68)(cid:85)(cid:68)(cid:80)(cid:72)(cid:87)(cid:72)(cid:85)(cid:86)(cid:73)(cid:82)(cid:85)(cid:51)(cid:39)(cid:48)(cid:35)(cid:20) (cid:11)(cid:70)(cid:12) (cid:53)(cid:72)(cid:79)(cid:68)(cid:87)(cid:76)(cid:82)(cid:81)(cid:69)(cid:72)(cid:87)(cid:90)(cid:72)(cid:72)(cid:81)(cid:47)(cid:82)(cid:70)(cid:68)(cid:79)(cid:76)(cid:93)(cid:68)(cid:87)(cid:76)(cid:82)(cid:81)(cid:36)(cid:70)(cid:70)(cid:17)(cid:9) ?
?
Figure4.IllustrationofPDM@K.(a)Differentretrievalmetriccomparison.Forclarityinthesamefigure,wehaveconvertedthespatial
distanced iofSDM@1toR iandthethresholdforRecall@1issetto0.5.(b)DifferentparametercombinationsforPDM@1.(c)Relation
betweenlocalizationaccuracyandR
i.ThiscurveisbasedontheactualAVLexperimentresults.
|     |     |     |     |     |     | form      | traditional |               | handcrafted |            | methods   | like          | SIFT     | and ORB.   |
| --- | --- | --- | --- | --- | --- | --------- | ----------- | ------------- | ----------- | ---------- | --------- | ------------- | -------- | ---------- |
|     |     |     |     |     |     | While     | ORB         | is            | fast        | and widely |           | used in       | SLAM     | [6], it    |
|     |     |     |     |     |     | struggles |             | with          | viewpoint   | changes.   |           | Additionally, |          | RoMa       |
|     |     |     |     |     |     | performs  |             | best          | among       | dense      | matching  | methods,      |          | whereas    |
|     |     |     |     |     |     | SP+LG     | GIM         | +k2s          | leads       | in sparse  | matching. |               | Overall, | dense      |
|     |     |     |     |     |     | methods   |             | significantly |             | surpass    | sparse    | methods       | in       | localiza-  |
|     |     |     |     |     |     | tion      | accuracy,   |               | but at      | the cost   | of lower  | computational |          | ef-        |
|     |     |     |     |     |     | ficiency  |             | (e.g.,        | RoMa        | takes      | over      | six times     | longer   | than       |
|     |     |     |     |     |     | SP+LG     |             | +k2s).        | Although    |            | DeDoDe    | attempts      |          | to address |
GIM
|     |     |     |     |     |     | this | issue, | it has | not | achieved | good | trade-off | in  | our test. |
| --- | --- | --- | --- | --- | --- | ---- | ------ | ------ | --- | -------- | ---- | --------- | --- | --------- |
Consequently,sparsematchingapproachesremainmoread-
vantageousforreal-timelocalizationtasks.
Figure5.VisualizationoftheRelationbetweenR
|     |     |     |     |     | iinPDM@K | 5.4.LocalizationStrategy |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | -------- | ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
andSubsequentLocalizationAccuracy.
|     |     |     |     |     |     | This                                  | section | compares |     | four | distinct | localization |              | strategies, |
| --- | --- | --- | --- | --- | --- | ------------------------------------- | ------- | -------- | --- | ---- | -------- | ------------ | ------------ | ----------- |
|     |     |     |     |     |     | theperformancemetricsareshowninTab.5. |         |          |     |      |          |              | Theretrieval |             |
matching accuracy. On the AnyVisLoc dataset, 竹 is rec- method employed was CAMP, and the matching method
| ommendedtobeintherangeof4to8. |     |     |     |     |     | wasSP+LG |            | GIM | +k2s.    |         |     |           |          |      |
| ----------------------------- | --- | --- | --- | --- | --- | -------- | ---------- | --- | -------- | ------- | --- | --------- | -------- | ---- |
|                               |     |     |     |     |     |          | The Direct |     | Matching | without |     | Retrieval | strategy | per- |
5.3.ImageMatchingApproach
|     |     |     |     |     |     | formed | the | worst. | In  | UAV AVL | tasks, | the | area | of the ref- |
| --- | --- | --- | --- | --- | --- | ------ | --- | ------ | --- | ------- | ------ | --- | ---- | ----------- |
erencemap(e.g.,9km2)isoftenmuchlargerthanthearea
| To evaluate | various | image | matching | approaches, | we con- |     |     |     |     |     |     |     |     |     |
| ----------- | ------- | ----- | -------- | ----------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ducted tests using CAMP and 19 matching methods. As oftheUAVimage(e.g.,0.04km2). Thisdiscrepancyleads
shown in Tab. 4, learning-based models generally outper- toredundantareasinthereferencemap, whichgreatlyex-
1736

Table4.LocalizationResultsofDifferentImageMatchingApproaches.?denotestheapproachesthatrunonCPU.
| ImageMatchingMethod |     |     |     |     | Top1+CAMP |     |     |     | Top5Re-rank+CAMP |     | RunTime |
| ------------------- | --- | --- | --- | --- | --------- | --- | --- | --- | ---------------- | --- | ------- |
A@5m A@7m A@10m A@15m A@20m A@5m A@7m A@10m A@15m A@20m ms/frame
SIFT[35] 43.9 50.1 55.7 59.9 62.5 52.5 59.4 64.5 68.4 70.8 316?
| ORB[6] |     |     |     | 3.9 | 5.8 | 8.0 10.9 | 13.6 | 5.4 | 7.6 10.3 | 13.8 17.2 | 44? |
| ------ | --- | --- | --- | --- | --- | -------- | ---- | --- | -------- | --------- | --- |
D2Net[17] 27.3 38.1 51.6 61.9 68.6 33.0 44.3 59.8 72.2 78.5 4083
ALIKE[62] 27.7 32.0 34.8 38.2 39.6 31.9 37.3 40.8 44.4 45.9 268
Xfeat*[39] 35.2 44.5 54.4 62.1 66.8 42.8 53.4 63.5 70.7 75.4 69
LiftFeat[33] 30.3 38.9 47.3 55.2 59.1 39.3 50.7 60.6 69.4 73.5 40
SP[15]+SG[41] 52.1 63.3 71.7 77.8 80.9 59.1 71.3 79.6 85.8 89.6 92
SP[15]+SG[41]+Omni[28] 45.3 55.0 64.2 72.3 76.1 52.2 63.6 72.9 81.3 84.8 3116?
SP[15]+LG[32] 46.6 55.8 63.5 68.7 71.7 55.7 66.5 76.2 81.9 85.4 76
SP[15]+LGMINIMA[32,40] 46.0 55.6 63.1 68.4 72.4 55.2 65.8 75.0 81.7 85.8 74
SP[15]+LGGIM[32,44] 55.8 66.7 75.0 81.6 85.1 62.4 73.5 82.2 88.9 92.4 75
SP[15]+LGGIM[32,44]+k2s[29] 57.0 67.6 75.4 81.7 84.8 62.9 74.8 83.2 89.2 91.8 105
XoFTRMINIMA[40,47] 48.3 54.7 60.2 63.4 65.8 59.4 66.8 72.9 77.4 80.0 68
LoFTRGIM[44,46] 59.5 67.4 74.1 79.1 81.6 65.9 74.9 82.5 87.2 89.1 165
DeDoDe[19] 51.5 61.8 69.1 74.8 77.2 61.3 71.6 79.0 84.4 86.9 291
DKMGIM[18,44] 65.6 73.8 80.2 84.0 86.4 68.5 78.1 85.0 90.3 92.1 4915
RoMaGIM[20,44] 60.3 66.5 71.4 74.7 76.2 68.2 74.6 81.7 86.7 88.6 655
RoMaMINIMA[20,40] 60.0 65.2 69.8 74.0 76.0 69.8 76.8 82.5 86.4 88.5 653
RoMa[20] 70.1 76.1 81.3 85.7 87.6 73.9 80.8 87.2 91.5 94.0 659
Table5.PerformanceMetricsofLocalizationStrategies
|                           |     |     |            |       |           |         | Overall,                   | Top             | N Re-rank | strategy has a | comprehensive |
| ------------------------- | --- | --- | ---------- | ----- | --------- | ------- | -------------------------- | --------------- | --------- | -------------- | ------------- |
|                           |     |     |            |       |           |         | advantage                  | in localization | accuracy, | computation    | time, and     |
| Strategy                  |     |     | A@5m A@10m | A@20m | s/frame   | storage | memoryusage.               |                 |           |                |               |
| Matching-wo-Retrieval[61] |     |     | 34.3       | 45.7  | 54.3 1.4  | Large   |                            |                 |           |                |               |
| Top1Matching[58]          |     |     | 55.8       | 74.3  | 84.0 0.3  | medium  |                            |                 |           |                |               |
|                           |     |     |            |       |           |         | 5.5.TheBestCombinedMethod: |                 |           | Baseline       |               |
| Top5Re-rank(N=5)[9]       |     |     | 62.2       | 82.4  | 91.5 0.8  | medium  |                            |                 |           |                |               |
| MostInliers[23]           |     |     | 64.0       | 83.2  | 92.6 10.2 | small   |                            |                 |           |                |               |
Basedontheaboveexperiments,thebestcombinedmethod
whichconsistsofCAMP+RoMa+TopNRerankwascho-
Table6.PerformanceMetricsforDifferentReferenceMaps
|     |                         |     |               |     |                  |     | sen as the                                     | baseline. | This baseline | was used | to test all data |
| --- | ----------------------- | --- | ------------- | --- | ---------------- | --- | ---------------------------------------------- | --------- | ------------- | -------- | ---------------- |
|     |                         |     |               |     |                  |     | intheAnyVisLocdataset,withresultsshowninTab.6. |           |               |          | Al-              |
| Map | SpatialResolution(Avg.) |     | RetrievalAcc. |     | LocalizationAcc. |     |                                                |           |               |          |                  |
thoughthebaselineshowedgoodaccuracyat94.2%within
|     | 2D-Reference | DSM | R@1 | P@1 | A@5m A@10m | A@20m |     |     |     |     |     |
| --- | ------------ | --- | --- | --- | ---------- | ----- | --- | --- | --- | --- | --- |
Aerial 0.070m 0.947m 61.6 0.922 74.1 87.7 94.2 20meters(ontheaerialmap),itonlyachieved74.1%accu-
| Satellite | 0.197m | 30m | 42.8 | 0.814 | 18.5 38.7 | 58.5 |     |     |     |     |     |
| --------- | ------ | --- | ---- | ----- | --------- | ---- | --- | --- | --- | --- | --- |
racywithin5meters,whichmaynotmeetthepreciseAVL
requirementsunderlow-altitude,multi-viewconditions.
pandsthesearchspaceofthematchingalgorithmandresult
6.FactorsAffectingtheBaselineAccuracy
inpoorlocalizationrobustness.
TheTop1Matchingstrategyusesimageretrievaltonar- This section discussed the main factors influencing the lo-
| rowthesearchspaceforsubsequentimagematching. |     |     |     |     |     | How- |                                         |     |     |     |                |
| -------------------------------------------- | --- | --- | --- | --- | --- | ---- | --------------------------------------- | --- | --- | --- | -------------- |
|                                              |     |     |     |     |     |      | calizationperformanceofcurrentbaseline. |     |     |     | Thefulldataset |
ever, due to the insufficient accuracy of existing image re- isusedtoconducttheexperiment.
| trieval | networks, | when | the Top1 | image | is not | the ground |     |     |     |     |     |
| ------- | --------- | ---- | -------- | ----- | ------ | ---------- | --- | --- | --- | --- | --- |
6.1.ReferenceMap
truth,thesubsequentmatchingalgorithmwillfail.
The Top N Re-rank strategy re-ranks the Top N re- Different reference maps exhibit different characteristics
trievalsbasedonthenumberofinliers. Thebasicassump- and localization accuracy (see Tab. 6). Satellite maps are
tionisthatimageswithmoreinliersareoftenclosertothe easier to obtain but significantly less accurate for localiza-
groundtruthandaremoresuitableforPnPproblemsolving.
|     |     |     |     |     |     |     | tion. Thisismainlycausedbytwofactors: |     |     |     | Firstly,satellite |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------- | --- | --- | --- | ----------------- |
Compared to the Top1 strategy, this strategy significantly maps have lower spatial resolution, especially with DSM
enhancesaccuracywithanacceptableincreaseintime. dataat30m.Underlow-altitudemulti-viewconditions,sub-
TheMostInliersstrategydirectlymatchestheUAVim- stantialelevationdifferencesinUAVimages(e.g.,rooftops
agewithallgalleryimagesandalsousesthenumberofin- vs. flat ground) require high-resolution DSM data (e.g.
< 1m)toensureaccuratePnPproblemsolving.
lierstosortretrievals. Althoughithasslightlyhigherlocal- Secondly,
ization accuracy than the Top N Re-Rank strategy, feature the significant temporal and modality differences between
matching for each gallery image is very time-consuming, UAVimagesandsatellitemapsposegreaterchallengesfor
makingitunabletomeetreal-timerequirements. imageretrievalandmatching(seeFig.6c).
1737

| (cid:56)(cid:36)(cid:57)(cid:44)(cid:80)(cid:68)(cid:74)(cid:72) |     | (cid:55)(cid:82)(cid:83)(cid:24)(cid:53)(cid:72)(cid:87)(cid:85)(cid:76)(cid:72)(cid:89)(cid:68)(cid:79)(cid:86)(cid:11)(cid:58)(cid:85)(cid:82)(cid:81)(cid:74)(cid:12) |     |     | (cid:42)(cid:85)(cid:82)(cid:88)(cid:71)(cid:55)(cid:85)(cid:88)(cid:87)(cid:75) |       |           |     |           |       |             |       |        |
| ---------------------------------------------------------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --- | --- | -------------------------------------------------------------------------------- | ----- | --------- | --- | --------- | ----- | ----------- | ----- | ------ |
|                                                                  |     |                                                                                                                                                                          |     |     |                                                                                  | Table | 7. Impact | of  | Different | Prior | Information | Noise | on the |
LocalizationAccuracy.Std:standarddeviation.
|     |     |     |     |     |     | YawStd | A@5m | A@10m | A@20m |     | PitchStd A@5m | A@10m | A@20m |
| --- | --- | --- | --- | --- | --- | ------ | ---- | ----- | ----- | --- | ------------- | ----- | ----- |
(cid:11)(cid:68)(cid:12)
|     |     |     |     |     |     |     | 0～ 74.6         | 87.6 | 94.2 |     | 0～ 74.6        | 87.6 | 94.2 |
| --- | --- | --- | --- | --- | --- | --- | --------------- | ---- | ---- | --- | -------------- | ---- | ---- |
|     |     |     |     |     |     |     | 5～ 74.3(∣0.3)   | 86.3 | 93.2 |     | 3～ 73.9(∣0.7)  | 87.2 | 94.2 |
|     |     |     |     |     |     |     | 10～ 72.7(∣1.9)  | 86.4 | 92.8 |     | 5～ 73.9(∣0.7)  | 87.1 | 93.2 |
|     |     |     |     |     |     |     | 20～ 72.4(∣2.2)  | 86.4 | 93.6 |     | 7～ 73.3(∣1.3)  | 87.3 | 93.4 |
|     |     |     |     |     |     |     | 70.5(∣4.1)      |      |      |     | 72.1(∣2.5)     |      |      |
|     |     |     |     |     |     |     | 30～             | 83.5 | 90.2 |     | 10～            | 86.5 | 92.2 |
|     |     |     |     |     |     |     | 50～ 60.9(∣13.7) | 72.8 | 79.5 |     | 20～ 71.6(∣3.0) | 86.2 | 92.9 |
|     |     |     |     |     |     |     | 60～ 48.9(∣25.7) | 63.0 | 70.0 |     | 30～ 69.7(∣4.9) | 83.7 | 90.4 |
|     |     |     |     |     |     |     | (a)YawNoise     |      |      |     | (b)PitchNoise  |      |      |
6.3.NoiseinPriorInformation
(cid:56)(cid:36)(cid:57)(cid:44)(cid:80)(cid:68)(cid:74)(cid:72) (cid:36)(cid:72)(cid:85)(cid:76)(cid:68)(cid:79)(cid:48)(cid:68)(cid:83) (cid:56)(cid:36)(cid:57)(cid:44)(cid:80)(cid:68)(cid:74)(cid:72) (cid:54)(cid:68)(cid:87)(cid:72)(cid:79)(cid:79)(cid:76)(cid:87)(cid:72)(cid:48)(cid:68)(cid:83) CurrentUAVplatformsgenerallycarrysensorsthatcanpro-
(cid:11)(cid:69)(cid:12) (cid:11)(cid:70)(cid:12) videinformationaboutpitch/yawanglesandaltitude(e.g.,
Figure 6. Challenging Cases for UAV AVL. The low-altitude gyroscopes and altimeters). In this paper, this information
|     |     |     |     |     |     | is  | used to | align the | UAV | image | and the reference |     | map to |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------- | --- | ----- | ----------------- | --- | ------ |
multi-viewconditionspresentgreaterchallengeforimageretrieval
(a)andimagematching(b).Temporalandmodalitydifferencesin similarrotationandscale,reducingthesearchspaceforre-
satellitemapsmakeslocalizationmoredifficult(c). trieval and matching. However, in the real scenarios, this
|        |      |         |          |              |           | prior                    | information |           | often contains | noise.                     | To       | analyze     | this is- |
| ------ | ---- | ------- | -------- | ------------ | --------- | ------------------------ | ----------- | --------- | -------------- | -------------------------- | -------- | ----------- | -------- |
|        |      |         |          |              |           | sue,                     | we added    | different | levels         | of                         | Gaussian | noise (mean | of       |
| Aerial | maps | provide | superior | localization | accuracy, |                          |             |           |                |                            |          |             |          |
|        |      |         |          |              |           | 0)tothepriorinformation. |             |           |                | TheresultsareshowninTab.7. |          |             |          |
however, pre-aerial photography and precise 3D modeling Whenstd >
Yawnoiseaffectstherotationestimation.
| oftheflightareaarerequired,makingthemlesssuitablefor |     |     |     |     |     | 10?, |     |     |     |     |     |     |     |
| ---------------------------------------------------- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
theaccuracyofexistingimageretrievalandmatching
time-sensitive missions (e.g., emergency rescue) or long- methodsissignificantlyaffected.Notably,thelargerthestd,
| distanceflighttasks. |     | Consequently,thechoiceofreference |     |     |     |                                                 |     |     |     |     |     |     |      |
| -------------------- | --- | --------------------------------- | --- | --- | --- | ----------------------------------------------- | --- | --- | --- | --- | --- | --- | ---- |
|                      |     |                                   |     |     |     | themoreseverelythelocalizationaccuracydeclines. |     |     |     |     |     |     | When |
maptypeshouldbetailoredtothespecificrequirementsof
thestdincreasesto30～and60～,A@5mdecreasesby4.1%
themissionathand.
and25.7%,respectively.
Tobetteranalyzetheimpactofotherfactors,thefollow-
|     |     |     |     |     |     |     | PitchnoiseaffectsthescaleestimationinEq.(3). |     |     |     |     |     | Low |
| --- | --- | --- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | --- | --- | --- |
ingexperimentsareconductedbasedontheaerialmap. pitchnoise(std < 5?)hasminimalimpactonlocalization
|     |     |     |     |     |     |           |     |          |          |       |           | (std | > 7?), |
| --- | --- | --- | --- | --- | --- | --------- | --- | -------- | -------- | ----- | --------- | ---- | ------ |
|     |     |     |     |     |     | accuracy. |     | However, | as pitch | noise | increases |      |        |
6.2.Multi-viewObservation
thesignificantscaledifferencecomplicatesimageretrieval
andmatching,leadingtoanoticeabledropinaccuracy,with
A@5mdecreasingby4.9%atstd=30?.
(cid:24)(cid:21)(cid:29)
|     |                              |     |     |     |     |     |     | altitude   |       | FOV |            | 2   |     |
| --- | ---------------------------- | --- | --- | --- | --- | --- | --- | ---------- | ----- | --- | ---------- | --- | --- |
|     | (cid:4)(cid:3)(cid:2)(cid:1) |     |     |     |     |     | r = |            | ﹞tan( |     | )﹞ (cid:2) |     | (3) |
|     | (cid:23)(cid:21)(cid:29)     |     |     |     |     |     |     | sin(pitch) |       | 2   | (w2+h2).   |     |     |
(cid:28)(cid:21)(cid:29)
|     |     |     |     |     |     |     | Altitude | noise | also affects | scale | estimation | like | pitch, |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----- | ------------ | ----- | ---------- | ---- | ------ |
butitsimpactissmall,thedetailsareputintheappendix.
|     | (cid:21)(cid:29) | (cid:20)(cid:21) (cid:20)(cid:22) (cid:23)(cid:21) | (cid:23)(cid:22) (cid:22)(cid:21) (cid:22)(cid:22) (cid:24)(cid:21) | (cid:24)(cid:22) (cid:25)(cid:21) (cid:25)(cid:22) (cid:26)(cid:21) (cid:26)(cid:22) | (cid:27)(cid:21) |     |     |     |     |     |     |     |     |
| --- | ---------------- | -------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:1)(cid:2)(cid:3)(cid:4)(cid:5)(cid:6)(cid:7)(cid:8)(cid:9)(cid:10)(cid:11)(cid:6)(cid:12)(cid:8)(cid:3)(cid:11)(cid:13)(cid:14)(cid:15)(cid:10)(cid:16)(cid:6)(cid:17)(cid:18)(cid:11)(cid:9)(cid:13)(cid:11)(cid:11)(cid:19)
7.Conclusion
| Figure7. | ImpactofPitchAngleonLocalizationAccuracy. |     |     |     | A   |     |     |     |     |     |     |     |     |
| -------- | ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
smallerpitchangletendstoreducelocalizationaccuracy.
ThispaperbenchmarksUAVAVLunderlow-altitudemulti-
|     |     |     |     |     |     | view | conditions. |     | The AnyVisLoc |     | dataset | is constructed |     |
| --- | --- | --- | --- | --- | --- | ---- | ----------- | --- | ------------- | --- | ------- | -------------- | --- |
Thissectionanalyzesthelocalizationresultsacrossdif- to facilitate comprehensive evaluation. A unified frame-
ferent pitch angles. As shown in Fig. 7, a smaller pitch workisintroducedtointegrateimage-levelretrieval,pixel-
angletendstoreducelocalizationaccuracy, indicatingthat levelmatchingmethods,andvariouslocalizationstrategies.
oblique-viewimagespresentgreaterchallengesforaccurate Based on this dataset and framework, state-of-the-art AVL
localizationcomparedtonadir-viewimages.Inlow-altitude approaches are exhaustively evaluated to select the best
flights, oblique-view images capture substantial side-view combined method as the baseline. Additionally, key fac-
information from 3D objects. These side-view details re- torsaffectingthebaselineperformancearethoroughlydis-
ducebothglobalandlocalsimilaritybetweenUAVimages cussed. Overall,thebaselinemethodachieveda74.1%ac-
andtheortho-referencemap.Consequently,theaccuracyof curacywithin5meters,indicatingsubstantialroomforim-
imageretrievalandmatchingalgorithmsisdiminished(see provementandhighlightingthepotentialofourbenchmark
Fig.6),makingpreciselocalizationmoredifficult. todrivefutureresearchinthisfield.
1738

References [15] Daniel DeTone, Tomasz Malisiewicz, and Andrew Rabi-
|     |     |     |     |     |     |     | novich. | Superpoint: | Self-supervisedinterestpointdetection |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ----------- | ------------------------------------- | --- | --- | --- | --- |
[1] Interimregulationsontheflightmanagementofunmanned anddescription. InCVPRw,2018. 2,4,7,6
| aerial vehicles.                         |     | https://www.gov.cn/zhengce/ |                          |         |              |     |               |         |          |          |              |            |          |
| ---------------------------------------- | --- | --------------------------- | ------------------------ | ------- | ------------ | --- | ------------- | ------- | -------- | -------- | ------------ | ---------- | -------- |
|                                          |     |                             |                          |         |              |     | [16] Fabian   | Deuser, | Konrad   | Habel,   | and Norbert  | Oswald.    | Sam-     |
| content/202306/content_6888799.htm,2023. |     |                             |                          |         |              | 2   |               |         |          |          |              |            |          |
|                                          |     |                             |                          |         |              |     | ple4geo:      | Hard    | negative | sampling | for          | cross-view | geo-     |
| [2] Relja Arandjelovic,                  |     | Petr                        | Gronat,                  | Akihiko | Torii, Tomas | Pa- |               |         |          |          |              |            |          |
|                                          |     |                             |                          |         |              |     | localisation. |         | In ICCV, | pages    | 16847每16856, | 2023.      | 2, 4, 5, |
| jdla,andJosefSivic.                      |     | Netvlad:                    | Cnnarchitectureforweakly |         |              |     | 6,3           |         |          |          |              |            |          |
supervised place recognition. In CVPR, pages 5297每5307, [17] MihaiDusmanu,IgnacioRocco,TomasPajdla,MarcPolle-
2016. 2,4,5,6
feys,JosefSivic,AkihikoTorii,andTorstenSattler.D2-Net:
| [3] Herbert Bay, | Tinne | Tuytelaars, |     | and Luc | Van Gool. | Surf: |     |     |     |     |     |     |     |
| ---------------- | ----- | ----------- | --- | ------- | --------- | ----- | --- | --- | --- | --- | --- | --- | --- |
ATrainableCNNforJointDetectionandDescriptionofLo-
| Speeded | up robust | features. | In  | ECCV, | pages 404每417. |     |              |     |              |     |       |     |     |
| ------- | --------- | --------- | --- | ----- | -------------- | --- | ------------ | --- | ------------ | --- | ----- | --- | --- |
|         |           |           |     |       |                |     | calFeatures. |     | InCVPR,2019. |     | 2,4,7 |     |     |
Springer,2006. 2 [18] Johan Edstedt, Ioannis Athanasiadis, Ma?rten Wadenba“ck,
[4] GabrieleBerton,RiccardoMereu,GabrieleTrivigno,Carlo
|                                            |                 |     |                 |     |               |     | and      | Michael | Felsberg. | DKM:        | Dense | kernelized | feature     |
| ------------------------------------------ | --------------- | --- | --------------- | --- | ------------- | --- | -------- | ------- | --------- | ----------- | ----- | ---------- | ----------- |
| Masone,                                    | GabrielaCsurka, |     | TorstenSattler, |     | andBarbaraCa- |     |          |         |           |             |       |            |             |
|                                            |                 |     |                 |     |               |     | matching | for     | geometry  | estimation. | In    | CVPR,      | 2023. 2, 4, |
| puto. Deepvisualgeo-localizationbenchmark. |                 |     |                 |     | InProceed-    |     |          |         |           |             |       |            |             |
7
ingsoftheIEEE/CVFConferenceonComputerVisionand
|     |     |     |     |     |     |     | [19] Johan | Edstedt, | Georg | Bo“kman, | Ma?rten |     | Wadenba“ck, |
| --- | --- | --- | --- | --- | --- | --- | ---------- | -------- | ----- | -------- | ------- | --- | ----------- |
PatternRecognition,pages5396每5407,2022. 2 and Michael Felsberg. Dedode: Detect, don＊t de-
| [5] Mollie Bianchi                   | and | Timothy | D   | Barfoot.           | Uav localization |     |                                                     |               |            |     |              |        |       |
| ------------------------------------ | --- | ------- | --- | ------------------ | ---------------- | --- | --------------------------------------------------- | ------------- | ---------- | --- | ------------ | ------ | ----- |
|                                      |     |         |     |                    |                  |     | scribe〞describe,don＊tdetectforlocalfeaturematching. |               |            |     |              |        | In    |
| usingautoencodedsatelliteimages.     |     |         |     | IEEERoboticsandAu- |                  |     |                                                     |               |            |     |              |        |       |
|                                      |     |         |     |                    |                  |     | 2024                                                | International | Conference |     | on 3D Vision | (3DV), | pages |
| tomationLetters,6(2):1761每1768,2021. |     |         |     | 1                  |                  |     |                                                     |               |            |     |              |        |       |
|                                      |     |         |     |                    |                  |     | 148每157.IEEE,2024.                                  |               | 7          |     |              |        |       |
[6] CarlosCampos, RichardElvira, JuanJ.Go?mezRodr??guez, [20] Johan Edstedt, Qiyu Sun, Georg Bo“kman, Ma?rten
Jose? M. M. Montiel, and Juan D. Tardo?s. Orb-slam3: An Wadenba“ck, and Michael Felsberg. RoMa: Robust Dense
| accurateopen-sourcelibraryforvisual, |       |           |              | visual每inertial, |           | and    |                              |      |            |       |                    |            |       |
| ------------------------------------ | ----- | --------- | ------------ | ---------------- | --------- | ------ | ---------------------------- | ---- | ---------- | ----- | ------------------ | ---------- | ----- |
|                                      |       |           |              |                  |           |        | FeatureMatching.             |      | CVPR,2024. |       | 2,4,7,6            |            |       |
| multimap                             | slam. | IEEE      | Transactions | on               | Robotics, | 37(6): |                              |      |            |       |                    |            |       |
|                                      |       |           |              |                  |           |        | [21] Wenjian                 | Gan, | Yang       | Zhou, | Xiaofei            | Hu, Luying | Zhao, |
| 1874每1890,2021.                      |       | 1,2,4,6,7 |              |                  |           |        |                              |      |            |       |                    |            |       |
|                                      |       |           |              |                  |           |        | GaoshuangHuang,andMingboHou. |      |            |       | Learningrobustfea- |            |       |
[7] YingxiuChang,YongqiangCheng,UmarManzoor,andJohn ture representation for cross-view image geo-localization.
Murray. A review of uav autonomous navigation in gps- IEEEGeoscienceandRemoteSensingLetters, 2025. 4, 5,
| denied environments. |     | Robotics |     | and Autonomous |     | Systems, |     |     |     |     |     |     |     |
| -------------------- | --- | -------- | --- | -------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
6
| page104533,2023. |     | 1   |     |     |     |     |                |      |           |     |                |     |           |
| ---------------- | --- | --- | --- | --- | --- | --- | -------------- | ---- | --------- | --- | -------------- | --- | --------- |
|                  |     |     |     |     |     |     | [22] Xiao-Shan | Gao, | Xiao-Rong |     | Hou, Jianliang |     | Tang, and |
[8] Jiahao Chen, Enhui Zheng, Ming Dai, Yifu Chen, and Hang-Fei Cheng. Complete solution classification for the
Yusheng Lu. Os-fpi: A coarse-to-fine one-stream network perspective-three-point problem. IEEE transactions on
foruavgeo-localization. IEEEJournalofSelectedTopicsin pattern analysis and machine intelligence, 25(8):930每943,
| AppliedEarthObservationsandRemoteSensing,2024. |     |     |     |     |     | 2   |       |     |     |     |     |     |     |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
|                                                |     |     |     |     |     |     | 2003. | 4   |     |     |     |     |     |
[9] ShuxiaoChen,XiangyuWu,MarkWMueller,andKoushil [23] Marius-MihailGurgu,JorgePen?aQueralta,andTomiWest-
Sreenath. Real-timegeo-localizationusingsatelliteimagery erlund. Vision-based gnss-free localization for uavs in the
and topography for unmanned aerial vehicles. In 2021 wild. In20227thInternationalConferenceonMechanical
IEEE/RSJ International Conference on Intelligent Robots EngineeringandRoboticsResearch(ICMERR),pages7每12.
| andSystems(IROS),pages2275每2281.IEEE,2021. |     |     |     |     |     | 4,7 |            |     |         |     |     |     |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | --- | ---------- | --- | ------- | --- | --- | --- | --- |
|                                            |     |     |     |     |     |     | IEEE,2022. |     | 2,3,4,7 |     |     |     |     |
[10] Yuan Chen and Jie Jiang. An oblique-robust absolute vi- [24] MengfanHe,JiachengLiu,PengfeiGu,andZiyangMeng.
suallocalizationmethodforgps-denieduavwithsatelliteim- Leveragingmapretrievalandalignmentforrobustuavvisual
agery. IEEETransactionsonGeoscienceandRemoteSens- geo-localization.IEEETransactionsonInstrumentationand
| ing,2023. | 1,2,3 |     |     |     |     |     | Measurement,2024. |     | 1   |     |     |     |     |
| --------- | ----- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- |
[11] ZhongweiChen,Zhao-XuYang,andHai-JunRong. Multi- [25] YaoHe,IvanCisneros,NikhilKeetha,JayPatrikar,ZelinYe,
level embedding and alignment network with consistency IanHiggins,YaoyuHu,ParvKapoor,andSebastianScherer.
and invariance learning for cross-view geo-localization. Foundloc: Vision-based onboard aerial localization in the
IEEE Transactions on Geoscience and Remote Sensing, wild. arXivpreprintarXiv:2310.16299,2023. 1
2025. 4,5,6
|     |     |     |     |     |     |     | [26] Shuyu | Hu, Zelin | Shi, Tong | Jin, | and Yunpeng | Liu. | Query- |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --------- | --------- | ---- | ----------- | ---- | ------ |
[12] Andy Couturier and Moulay A Akhloufi. A review on ab- drivenfeaturelearningforcross-viewgeo-localization.IEEE
solutevisuallocalizationforuav. RoboticsandAutonomous TransactionsonGeoscienceandRemoteSensing, 2025. 4,
| Systems,135:103666,2021. |     |     | 1,3 |     |     |     | 5,6 |     |     |     |     |     |     |
| ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
[13] MingDai,JianhongHu,JiedongZhuang,andEnhuiZheng. [27] Yuxiang Ji, Boyong He, Zhuoyue Tan, and Liaoni Wu.
Atransformer-basedfeaturesegmentationandregionalign- Game4loc: A uav geo-localization benchmark from game
mentmethodforuav-viewgeo-localization. IEEETCSVT, data. In Proceedings of the AAAI Conference on Artificial
32(7):4376每4389,2021. 2,4,5,6 Intelligence,pages3913每3921,2025. 3
[14] Ming Dai, Enhui Zheng, Zhenhua Feng, Lei Qi, Jiedong [28] Hanwen Jiang, Arjun Karpur, Bingyi Cao, Qixing Huang,
Zhuang, and Wankou Yang. Vision-based uav self- andAndre?Araujo. Omniglue:Generalizablefeaturematch-
positioninginlow-altitudeurbanenvironments.IEEETrans- ing with foundation model guidance. In CVPR, pages
actionsonImageProcessing,2023. 1,2,3,4,5,6 19865每19875,2024. 2,4,7
1739

[29] ShinjeongKim,MarcPollefeys,andDanielBarath. Learn- [43] Tianrui Shen, Yingmei Wei, Lai Kang, Shanshan Wan,
ingtomakekeypointssub-pixelaccurate. InECCV,2024. and Yee-Hong Yang. Mccg: A convnext-based multiple-
2,4,7 classifier method for cross-view geo-localization. IEEE
[30] HuiLi,JiayangZhao,BingqiYan,LinweiYue,andLunche TCSVT,2023. 2,4,5,6
Wang. Global dems vary from one to another: an evalua- [44] XuelunShen,ZhipengCai,WeiYin,MatthiasMu“ller,Zijun
tionofnewlyreleasedcopernicus,nasaandaw3d30demon Li,KaixuanWang,XiaozhiChen,andChengWang. Gim:
selectedterrainsofchinausingicesat-2altimetrydata.Inter- Learninggeneralizableimagematcherfrominternetvideos.
national Journal of Digital Earth, 15(1):1149每1168, 2022. InICLR,2024. 4,7,5,6
2 [45] Woo-Hyuck Song, Hong-Gyu Jung, In-Youb Gwak, and
[31] Jinliang Lin, Zhedong Zheng, Zhun Zhong, Zhiming Luo, Seong-Whan Lee. Oblique aerial image matching based
Shaozi Li, Yi Yang, and Nicu Sebe. Joint representa- oniterativesimulationandhomographyevaluation. Pattern
tion learning and keypoint detection for cross-view geo- Recognition,87:317每331,2019. 2,3
localization. IEEETransactionsonImageProcessing(TIP), [46] Jiaming Sun, Zehong Shen, Yuang Wang, Hujun Bao, and
2022. 2,4,5,6 XiaoweiZhou. Loftr: Detector-freelocalfeaturematching
[32] PhilippLindenberger,Paul-EdouardSarlin,andMarcPolle- withtransformers. InCVPR,2021. 2,4,7
feys. LightGlue:LocalFeatureMatchingatLightSpeed. In [47] O“nder Tuzcuog?lu, Aybora Ko“ksal, Bug?ra Sofu, Sinan
ICCV,2023. 2,4,7,6 Kalkan, and A Aydin Alatan. Xoftr: Cross-modal feature
matchingtransformer.InProceedingsoftheIEEE/CVFCon-
[33] Yepeng Liu, Wenpeng Lai, Zhou Zhao, Yuxuan Xiong,
ferenceonComputerVisionandPatternRecognition,pages
Jinchi Zhu, Jun Cheng, and Yongchao Xu. Liftfeat: 3d
4275每4286,2024. 4,7
geometry-aware local feature matching. In 2025 IEEE In-
ternationalConferenceonRoboticsandAutomation(ICRA), [48] GeraldJVanDalen,DanielPMagree,andEricNJohnson.
pages11714每11720,2025. 4,7 Absolutelocalizationusingimagealignmentandparticlefil-
tering. InAIAAGuidance,Navigation,andControlConfer-
[34] ZhuangLiu,HanziMao,Chao-YuanWu,ChristophFeicht-
ence,page0647,2016. 2,4,5,6
enhofer,TrevorDarrell,andSainingXie. Aconvnetforthe
[49] Chengyi Wang, Jingbo Chen, Jiansheng Chen, Anzhi Yue,
2020s. CVPR,2022. 5
Dongxu He, Qingqing Huang, and Yi Zhang. Unmanned
[35] D.G.Lowe. Distinctiveimagefeaturesfromscale-invariant
aerialvehicleobliqueimageregistrationusinganasift-based
keypoints. Int.J.Comput.Vis.,60(2):91每110,2004. 2,4,7
matching method. Journal of Applied Remote Sensing, 12
[36] XiaoyongLuandSonglinDu. Raisingtheceiling:Conflict-
(2):025002每025002,2018. 3
freelocalfeaturematchingwithdynamicviewswitching. In
[50] Tingyu Wang, Zhedong Zheng, Chenggang Yan, Jiyong
ECCV,pages256每273.Springer,2024. 2
Zhang, Yaoqi Sun, Bolun Zheng, and Yi Yang. Each
[37] Muhammad Hamza Mughal, Muhammad Jawad Khokhar,
part matters: Local patterns facilitate cross-view geo-
and Muhammad Shahzad. Assisting uav localization via
localization. IEEE TCSVT, 32(2):867每879, 2021. 2, 4, 5,
deepcontextualimagematching. IEEEJournalofSelected
6,3
TopicsinAppliedEarthObservationsandRemoteSensing,
[51] YifanWang,XingyiHe,SidaPeng,DongliTan,andXiaowei
14:2445每2457,2021. 1,2,3
Zhou.Efficientloftr:Semi-denselocalfeaturematchingwith
[38] Konstantinos G Nikolakopoulos. Accuracy assessment of sparse-likespeed. InCVPR,pages21666每21675,2024. 2
alosaw3d30dsmandcomparisontoalosprismdsmcreated
[52] Zhen Wang, Dianxi Shi, Chunping Qiu, Songchang Jin,
withclassicalphotogrammetrictechniques. EuropeanJour-
Tongyue Li, Yanyan Shi, Zhe Liu, and Ziteng Qiao. Se-
nalofRemoteSensing,53(sup2):39每52,2020. 2
quencematchingforimage-baseduav-to-satellitegeolocal-
[39] GuilhermePotje,FelipeCadar,Andre? Araujo,RenatoMar- ization.IEEETransactionsonGeoscienceandRemoteSens-
tins, and Erickson R Nascimento. Xfeat: Accelerated fea- ing,2024. 1
turesforlightweightimagematching.InCVPR,pages2682每 [53] Qiong Wu, Yi Wan, Zhi Zheng, Yongjun Zhang, Guang-
2691,2024. 2,4,7 shuai Wang, and Zhenyang Zhao. Camp: A cross-view
[40] Jiangwei Ren, Xingyu Jiang, Zizhuo Li, Dingkang Liang, geo-localizationmethodusingcontrastiveattributesmining
XinZhou,andXiangBai. MINIMA:Modalityinvariantim- andposition-awarepartitioning. IEEETransactionsonGeo-
agematching. InProceedingsoftheIEEE/CVFConference scienceandRemoteSensing,2024. 2,4,5,6
onComputerVisionandPatternRecognition,pages23059每 [54] RouwanWu,XiaoyaCheng,JuelinZhu,XuxiangLiu,Mao-
23068.Piscataway:IEEE,2025. 4,7,6 junZhang,andShenYan. Uavd4l: Alarge-scaledatasetfor
[41] Paul-Edouard Sarlin, Daniel DeTone, Tomasz Malisiewicz, uav 6-dof localization. In International Conference on 3D
and Andrew Rabinovich. SuperGlue: Learning feature Vision(3DV),2024. 3
matching with graph neural networks. In CVPR, 2020. 2, [55] PanwangXia,YiWan,ZhiZheng,YongjunZhang,andJiwei
4,7 Deng. Enhancingcross-viewgeo-localizationwithdomain
[42] Michael Schleiss, Fahmi Rouatbi, and Daniel Cremers. alignmentandsceneconsistency. IEEETCSVT,2024. 2,4,
Vpair-aerial visual place recognition and localization in 5,6
large-scaleoutdoorenvironments. arXiv:2205.11567,2022. [56] Wenjia Xu, Yaxuan Yao, Jiaqi Cao, Zhiwei Wei, Chunbo
1,3 Liu, Jiuniu Wang, and Mugen Peng. Uav-visloc: A large-
1740

scale dataset for uav visual localization. arXiv preprint
arXiv:2405.11936,2024. 2,3
[57] NianXue,LiangNiu,XianbinHong,ZhenLi,LarissaHof-
faeller, and Christina Po“pper. Deepsim: Gps spoofing de-
tection on uavs using satellite imagery matching. In Pro-
ceedingsofthe36thAnnualComputerSecurityApplications
Conference,page304每319,NewYork,NY,USA,2020.As-
sociationforComputingMachinery. 1
[58] QinYe,JunqiLuo,andYiLin. Acoarse-to-finevisualgeo-
localization method for gnss-denied uav with oblique-view
imagery. ISPRS Journal of Photogrammetry and Remote
Sensing,212:306每322,2024. 2,3,4,7
[59] Peng Yin, Ivan Cisneros, Shiqi Zhao, Ji Zhang, Howie
Choset,andSebastianScherer. isimloc:Visualgloballocal-
ization for previously unseen environments with simulated
images. IEEETransactionsonRobotics,39(3):1893每1909,
2023. 2
[60] Aurelien Yol, Bertrand Delabarre, Amaury Dame, Jean-
Emile Dartois, and Eric Marchand. Vision-based absolute
localizationforunmannedaerialvehicles.In2014IEEE/RSJ
InternationalConferenceonIntelligentRobotsandSystems,
pages3429每3434.IEEE,2014. 2,4,5,6
[61] YijieYuan,WeiHuang,XiangxinWang,HuaiyuXu,Hongy-
ing Zuo, and Ruidan Su. Automated accurate registration
methodbetweenuavimageandgooglesatellitemap. Mul-
timediaToolsandApplications,79:16573每16591,2020. 4,
7
[62] Xiaoming Zhao, Xingming Wu, Jinyu Miao, Weihai Chen,
Peter CY Chen, and Zhengguo Li. Alike: Accurate and
lightweight keypoint detection and descriptor extraction.
IEEETransactionsonMultimedia,25:3101每3112,2022. 2,
4,7
[63] Zhedong Zheng, Yunchao Wei, and Yi Yang. University-
1652: A multi-view multi-source benchmark for drone-
based geo-localization. In Proceedings of the 28th ACM
internationalconferenceonMultimedia, pages1395每1403,
2020. 2,3,4
[64] XinZhou,XuerongYang,andYanchunZhang. Cdm-net:A
frameworkforcross-viewgeo-localizationwithmultimodal
data.IEEETransactionsonGeoscienceandRemoteSensing,
2025. 3
[65] Runzhe Zhu, Ling Yin, Mingze Yang, Fei Wu, Yuncheng
Yang, and Wenbo Hu. Sues-200: A multi-height multi-
scenecross-viewimagebenchmarkacrossdroneandsatel-
lite. IEEETCSVT,33(9):4825每4839,2023. 2,3
1741
