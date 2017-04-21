import numpy
import skimage.color

import cellprofiler.module
import cellprofiler.setting


__doc__ = """
Create an RGB image with color-coded labels overlaid on a grayscale image.
"""


class OverlayObjects(cellprofiler.module.ImageProcessing):
    module_name = "OverlayObjects"

    variable_revision_number = 1

    def create_settings(self):
        super(OverlayObjects, self).create_settings()

        self.x_name.text = "Input"

        self.x_name.doc = "Objects will be overlaid on this image."

        self.y_name.doc = "An RGB image with color-coded labels overlaid on a grayscale image."

        self.objects = cellprofiler.setting.ObjectNameSubscriber(
            text="Objects",
            doc="Color-coded labels of this object will be overlaid on the input image."
        )

        self.opacity = cellprofiler.setting.Float(
            text="Opacity",
            value=0.3,
            minval=0.0,
            maxval=1.0,
            doc="""
            Opacity of overlaid labels. Increase this value to descrease the transparency of the colorized object
            labels.
            """
        )

    def settings(self):
        settings = super(OverlayObjects, self).settings()

        settings += [
            self.objects,
            self.opacity
        ]

        return settings

    def visible_settings(self):
        visible_settings = super(OverlayObjects, self).visible_settings()

        visible_settings += [
            self.objects,
            self.opacity
        ]

        return visible_settings

    def run(self, workspace):
        self.function = lambda pixel_data, objects_name, opacity: overlay_objects(
            pixel_data,
            workspace.object_set.get_objects(objects_name),
            opacity
        )

        super(OverlayObjects, self).run(workspace)

    def display(self, workspace, figure, cmap=["gray", None]):
        super(OverlayObjects, self).display(workspace, figure, cmap=["gray", None])


def overlay_objects(pixel_data, objects, opacity):
    labels = objects.segmented

    if objects.volumetric:
        overlay = numpy.zeros(labels.shape + (3,), dtype=numpy.float32)

        for index, plane in enumerate(pixel_data):
            overlay[index] = skimage.color.label2rgb(
                labels[index],
                image=plane,
                alpha=opacity,
                bg_label=0
            )

        return overlay

    return skimage.color.label2rgb(
        labels,
        image=pixel_data,
        alpha=opacity,
        bg_label=0
    )
