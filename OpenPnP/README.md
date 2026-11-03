# OpenPnP Vision Pipelines Collection

Tổng hợp các vision pipeline Openpnp.

---

## 1. Bottom Vision Pipelines

Default Machine Bottom Vision

```xml
<cv-pipeline>
   <stages>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ParameterNumeric" name="pThreshold" enabled="true" parameter-label="Threshold" parameter-description="Set the brightness threshold that isolates the shiny contacts of a part." stage-name="threshold" property-name="threshold" effect-stage-name="threshold" preview-result="true" minimum-value="1.0" maximum-value="254.0" default-value="100.0" numeric-type="Integer"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ParameterNumeric" name="pDetail" enabled="true" parameter-label="Min. Detail Size" parameter-description="Minimal size of a detail that should be included in the detected shape." stage-name="filterContours" property-name="minArea" effect-stage-name="contours" preview-result="true" minimum-value="0.0" maximum-value="0.25" default-value="0.01" numeric-type="SquareMillimetersToPixels"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageCapture" name="0" enabled="true" default-light="true" settle-option="Skip" count="1">
         <light class="java.lang.String">1</light>
      </cv-stage>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageWriteDebug" name="deb0" enabled="true" prefix="bv_source_" suffix=".png"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.BlurGaussian" name="3" enabled="true" kernel-size="9" property-name="BlurGaussian"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskCircle" name="4" enabled="true" diameter="525" property-name="MaskCircle"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskCircle" name="4b" enabled="true" diameter="150" property-name="partmask"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ConvertColor" name="5" enabled="true" conversion="Bgr2HsvFull"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskHsv" name="6" enabled="true" auto="false" fraction-to-mask="0.0" hue-min="60" hue-max="130" saturation-min="32" saturation-max="255" value-min="64" value-max="255" soft-edge="0" soft-factor="1.0" invert="false" binary-mask="false" property-name="MaskHsv"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ConvertColor" name="7" enabled="true" conversion="Hsv2BgrFull"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ConvertColor" name="8" enabled="true" conversion="Bgr2Gray"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.Threshold" name="threshold" enabled="true" threshold="100" auto="true" invert="false"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.FindContours" name="findCountours" enabled="true" retrieval-mode="List" approximation-method="None"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.FilterContours" name="filterContours" enabled="true" contours-stage-name="findCountours" min-area="8.91821276636579" max-area="50.0" property-name="FilterContours"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskCircle" name="11" enabled="true" diameter="50" property-name=""/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.DrawContours" name="contours" enabled="true" contours-stage-name="filterContours" thickness="1" index="-1">
         <color r="255" g="255" b="255" a="255"/>
      </cv-stage>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MinAreaRect" name="results" enabled="true" threshold-min="100" threshold-max="255" expected-angle="0.0" search-angle="45.0" left-edge="true" right-edge="true" top-edge="true" bottom-edge="true" diagnostics="false" property-name="MinAreaRect"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageRecall" name="14" enabled="true" image-stage-name="0"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.DrawRotatedRects" name="15" enabled="true" rotated-rects-stage-name="results" thickness="2" draw-rect-center="false" rect-center-radius="20" show-orientation="false"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageWriteDebug" name="deb1" enabled="true" prefix="bv_result_" suffix=".png"/>
   </stages>
</cv-pipeline>
```

Nozzle Juki-503

```xml
<cv-pipeline>
  <stages>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageCapture" name="image" enabled="true" default-light="true" settle-option="Settle" count="1"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskCircle" name="mask" enabled="true" diameter="100" property-name="MaskCircle"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.DetectCircularSymmetry" name="cir" enabled="true" min-diameter="11" max-diameter="14" max-distance="250" search-width="0" search-height="0" max-target-count="1" min-symmetry="1.2" corr-symmetry="0.0" outer-margin="0.2" inner-margin="0.4" sub-sampling="8" super-sampling="1" symmetry-score="OverallVarianceVsRingVarianceSum" property-name="" diagnostics="true" heat-map="true"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ConvertModelToKeyPoints" name="results" enabled="true" model-stage-name="cir"/>
  </stages>
</cv-pipeline>
```

---

R0603 / C0603

```xml
<cv-pipeline>
   <stages>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageCapture" name="CaptureImage" enabled="true" default-light="false" settle-option="Skip" count="1">
         <light class="java.lang.String">0.1</light>
      </cv-stage>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageWriteDebug" name="SaveDebugImage" enabled="true" prefix="bv_source_" suffix=".png"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskCircle" name="MaskCircle" enabled="true" diameter="85" property-name=""/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskHsv" name="RemoveGreen" enabled="true" auto="true" fraction-to-mask="0.0" hue-min="-1" hue-max="-1" saturation-min="-1" saturation-max="-1" value-min="-1" value-max="-1" soft-edge="1" soft-factor="1.0" invert="false" binary-mask="false" property-name="MaskHsv"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ConvertColor" name="ConvertToGray" enabled="true" conversion="Bgr2Gray"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.BlurGaussian" name="InitialBlur" enabled="true" kernel-size="9" property-name="BlurGaussian"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.Threshold" name="Threshold" enabled="true" threshold="200" auto="false" invert="false"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MinAreaRect" name="results" enabled="true" threshold-min="150" threshold-max="255" expected-angle="0.0" search-angle="45.0" left-edge="true" right-edge="true" top-edge="true" bottom-edge="true" diagnostics="false" property-name="MinAreaRect"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageRecall" name="RecallOriginal" enabled="true" image-stage-name="CaptureImage"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.DrawRotatedRects" name="DrawRectangle" enabled="true" rotated-rects-stage-name="results" thickness="2" draw-rect-center="false" rect-center-radius="20" show-orientation="false"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageWriteDebug" name="SaveDebugWithCV" enabled="false" prefix="bv_result_" suffix=".png"/>
   </stages>
</cv-pipeline>
```
R1206 / C1206 / C1210

```xml
<cv-pipeline>
   <stages>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ParameterNumeric" name="pThreshold" enabled="true" parameter-label="Threshold" parameter-description="Set the brightness threshold that isolates the shiny contacts of a part." stage-name="threshold" property-name="threshold" effect-stage-name="threshold" preview-result="true" minimum-value="1.0" maximum-value="254.0" default-value="100.0" numeric-type="Integer"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ParameterNumeric" name="pDetail" enabled="true" parameter-label="Min. Detail Size" parameter-description="Minimal size of a detail that should be included in the detected shape." stage-name="filterContours" property-name="minArea" effect-stage-name="contours" preview-result="true" minimum-value="0.0" maximum-value="0.25" default-value="0.01" numeric-type="SquareMillimetersToPixels"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageCapture" name="0" enabled="true" default-light="false" settle-option="Skip" count="1">
         <light class="java.lang.String">0.25</light>
      </cv-stage>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageWriteDebug" name="deb0" enabled="true" prefix="bv_source_" suffix=".png"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.BlurGaussian" name="3" enabled="true" kernel-size="9" property-name="BlurGaussian"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskCircle" name="4" enabled="true" diameter="525" property-name="MaskCircle"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskCircle" name="4b" enabled="true" diameter="150" property-name="partmask"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ConvertColor" name="5" enabled="true" conversion="Bgr2HsvFull"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskHsv" name="6" enabled="true" auto="false" fraction-to-mask="0.0" hue-min="60" hue-max="130" saturation-min="32" saturation-max="255" value-min="64" value-max="255" soft-edge="0" soft-factor="1.0" invert="false" binary-mask="false" property-name="MaskHsv"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ConvertColor" name="7" enabled="true" conversion="Hsv2BgrFull"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ConvertColor" name="8" enabled="true" conversion="Bgr2Gray"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.Threshold" name="threshold" enabled="true" threshold="100" auto="true" invert="false"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.FindContours" name="findCountours" enabled="true" retrieval-mode="List" approximation-method="None"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.FilterContours" name="filterContours" enabled="true" contours-stage-name="findCountours" min-area="8.91821276636579" max-area="50.0" property-name="FilterContours"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskCircle" name="11" enabled="true" diameter="165" property-name=""/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.DrawContours" name="contours" enabled="true" contours-stage-name="filterContours" thickness="1" index="-1">
         <color r="255" g="255" b="255" a="255"/>
      </cv-stage>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MinAreaRect" name="results" enabled="true" threshold-min="100" threshold-max="255" expected-angle="0.0" search-angle="45.0" left-edge="true" right-edge="true" top-edge="true" bottom-edge="true" diagnostics="false" property-name="MinAreaRect"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageRecall" name="14" enabled="true" image-stage-name="0"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.DrawRotatedRects" name="15" enabled="true" rotated-rects-stage-name="results" thickness="2" draw-rect-center="false" rect-center-radius="20" show-orientation="false"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageWriteDebug" name="deb1" enabled="true" prefix="bv_result_" suffix=".png"/>
   </stages>
</cv-pipeline>
```

---

## 2. Fiducial Pipelines

FIDUCIAL-HOME_1

```xml
<cv-pipeline>
   <stages>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ParameterNumeric" name="maxDistance" enabled="true" parameter-label="Max. Distance" parameter-description="Maximum allowed distance between nominal fiducial location and detected location." stage-name="circular" property-name="maxDistance" effect-stage-name="circular" preview-result="true" minimum-value="0.0" maximum-value="10.0" default-value="4.0" numeric-type="MillimetersToPixels"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageCapture" name="image" enabled="true" default-light="false" settle-option="Skip" count="1">
         <light class="java.lang.String">1</light>
      </cv-stage>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageWriteDebug" name="deb0" enabled="false" prefix="fidloc_source_" suffix=".png"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.BlurGaussian" name="blur" enabled="false" kernel-size="3" property-name="BlurGaussian"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.DetectCircularSymmetry" name="circular" enabled="true" min-diameter="10" max-diameter="100" max-distance="125" search-width="300" search-height="300" max-target-count="1" min-symmetry="1.2" corr-symmetry="0.0" outer-margin="0.2" inner-margin="0.4" sub-sampling="8" super-sampling="8" symmetry-score="OverallVarianceVsRingVarianceSum" property-name="fiducial" diagnostics="true" heat-map="false"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageRecall" name="0" enabled="true" image-stage-name="image"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ConvertModelToKeyPoints" name="results" enabled="true" model-stage-name="circular"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.DrawCircles" name="draw" enabled="true" circles-stage-name="circular" thickness="2">
         <color r="255" g="255" b="0" a="255"/>
         <center-color r="255" g="0" b="0" a="255"/>
      </cv-stage>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageWriteDebug" name="deb1" enabled="false" prefix="fidloc_results_" suffix=".png"/>
   </stages>
</cv-pipeline>
```

FIDUCIAL-HOME_2

```xml
<cv-pipeline>
   <stages>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageCapture" name="image" enabled="true" default-light="true" settle-option="Settle" count="1"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskRectangle" name="maskR" enabled="false" width="670" height="335"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskCircle" name="maskC" enabled="false" diameter="600" property-name="MaskCircle"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.DetectCircularSymmetry" name="cir" enabled="true" min-diameter="10" max-diameter="60" max-distance="150" search-width="0" search-height="0" max-target-count="1" min-symmetry="1.2" corr-symmetry="0.0" outer-margin="0.2" inner-margin="0.4" sub-sampling="8" super-sampling="1" symmetry-score="OverallVarianceVsRingVarianceSum" property-name="" diagnostics="true" heat-map="false"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ConvertModelToKeyPoints" name="results" enabled="true" model-stage-name="cir"/>
   </stages>
</cv-pipeline>
```

Fiducial 1mm Mask 2mm

```xml
<cv-pipeline>
   <stages>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ImageCapture" name="image" enabled="true" default-light="true" settle-option="Settle" count="1"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.MaskCircle" name="mask" enabled="false" diameter="120" property-name="MaskCircle"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.DetectCircularSymmetry" name="cir" enabled="true" min-diameter="10" max-diameter="50" max-distance="50" search-width="0" search-height="0" max-target-count="1" min-symmetry="1.2" corr-symmetry="0.0" outer-margin="0.2" inner-margin="0.4" sub-sampling="8" super-sampling="1" symmetry-score="OverallVarianceVsRingVarianceSum" property-name="" diagnostics="true" heat-map="false"/>
      <cv-stage class="org.openpnp.vision.pipeline.stages.ConvertModelToKeyPoints" name="results" enabled="true" model-stage-name="cir"/>
   </stages>
</cv-pipeline>
```
