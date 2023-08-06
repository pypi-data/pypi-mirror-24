# pylint: disable=I0011,W0613,W0201,W0212,E1101,E1103

from __future__ import absolute_import, division, print_function

import os
from collections import Counter

import pytest

from astropy.wcs import WCS

import numpy as np
from numpy.testing import assert_allclose

from glue.core.coordinates import Coordinates, WCSCoordinates
from glue.core.message import SubsetUpdateMessage
from glue.core import HubListener, Data
from glue.core.roi import XRangeROI, RectangularROI
from glue.core.subset import RoiSubsetState
from glue.utils.qt import combo_as_string
from glue.viewers.matplotlib.qt.tests.test_data_viewer import BaseTestMatplotlibDataViewer
from glue.core.state import GlueUnSerializer
from glue.app.qt.layer_tree_widget import LayerTreeWidget
from glue.viewers.scatter.state import ScatterLayerState
from glue.viewers.image.state import ImageLayerState, ImageSubsetLayerState
from glue.core.link_helpers import LinkSame
from glue.app.qt import GlueApplication

from ..data_viewer import ImageViewer

DATA = os.path.join(os.path.dirname(__file__), 'data')


class TestImageCommon(BaseTestMatplotlibDataViewer):

    def init_data(self):
        return Data(label='d1', x=np.arange(12).reshape((3, 4)), y=np.ones((3, 4)))

    viewer_cls = ImageViewer

    def setup_method(self, method):
        # Some of the tests rely on seeing whether the viewer updates if we
        # change the color of the data, so we temporarily set it so that
        # global_sync is True in each layer (otherwise changing the color of)
        # a dataset has no effect on the image viewer specifically. We change
        # it back in teardown_method.
        ImageLayerState.global_sync._default = True
        return super(TestImageCommon, self).setup_method(method)

    def teardown_method(self, method):
        ImageLayerState.global_sync._default = False

    @pytest.mark.skip()
    def test_double_add_ignored(self):
        pass


class MyCoords(Coordinates):
    def axis_label(self, i):
        return ['Banana', 'Apple'][i]


class TestImageViewer(object):

    def setup_method(self, method):

        self.coords = MyCoords()
        self.image1 = Data(label='image1', x=[[1, 2], [3, 4]], y=[[4, 5], [2, 3]])
        self.image2 = Data(label='image2', a=[[3, 3], [2, 2]], b=[[4, 4], [3, 2]],
                           coords=self.coords)
        self.catalog = Data(label='catalog', c=[1, 3, 2], d=[4, 3, 3])
        self.hypercube = Data(label='hypercube', x=np.arange(120).reshape((2, 3, 4, 5)))

        # Create data versions with WCS coordinates
        self.image1_wcs = Data(label='image1_wcs', x=self.image1['x'],
                               coords=WCSCoordinates(wcs=WCS(naxis=2)))
        self.hypercube_wcs = Data(label='hypercube_wcs', x=self.hypercube['x'],
                                  coords=WCSCoordinates(wcs=WCS(naxis=4)))

        self.application = GlueApplication()

        self.session = self.application.session

        self.hub = self.session.hub

        self.data_collection = self.session.data_collection
        self.data_collection.append(self.image1)
        self.data_collection.append(self.image2)
        self.data_collection.append(self.catalog)
        self.data_collection.append(self.hypercube)
        self.data_collection.append(self.image1_wcs)
        self.data_collection.append(self.hypercube_wcs)

        self.viewer = ImageViewer(self.session)

        self.data_collection.register_to_hub(self.hub)
        self.viewer.register_to_hub(self.hub)

        self.options_widget = self.viewer.options_widget()

    def teardown_method(self, method):
        self.viewer.close()

    def test_basic(self):

        # Check defaults when we add data

        self.viewer.add_data(self.image1)

        assert combo_as_string(self.options_widget.ui.combosel_x_att_world) == 'World 0:World 1'
        assert combo_as_string(self.options_widget.ui.combosel_y_att_world) == 'World 0:World 1'

        assert self.viewer.axes.get_xlabel() == 'World 1'
        assert self.viewer.state.x_att_world is self.image1.id['World 1']
        assert self.viewer.state.x_att is self.image1.pixel_component_ids[1]
        # TODO: make sure limits are deterministic then update this
        # assert self.viewer.state.x_min == -0.5
        # assert self.viewer.state.x_max == +1.5

        assert self.viewer.axes.get_ylabel() == 'World 0'
        assert self.viewer.state.y_att_world is self.image1.id['World 0']
        assert self.viewer.state.y_att is self.image1.pixel_component_ids[0]
        # TODO: make sure limits are deterministic then update this
        # assert self.viewer.state.y_min == -0.5
        # assert self.viewer.state.y_max == +1.5

        assert not self.viewer.state.x_log
        assert not self.viewer.state.y_log

        assert len(self.viewer.state.layers) == 1

    def test_custom_coords(self):

        # Check defaults when we add data with coordinates

        self.viewer.add_data(self.image2)

        assert combo_as_string(self.options_widget.ui.combosel_x_att_world) == 'Banana:Apple'
        assert combo_as_string(self.options_widget.ui.combosel_x_att_world) == 'Banana:Apple'

        assert self.viewer.axes.get_xlabel() == 'Apple'
        assert self.viewer.state.x_att_world is self.image2.id['Apple']
        assert self.viewer.state.x_att is self.image2.pixel_component_ids[1]
        assert self.viewer.axes.get_ylabel() == 'Banana'
        assert self.viewer.state.y_att_world is self.image2.id['Banana']
        assert self.viewer.state.y_att is self.image2.pixel_component_ids[0]

    def test_flip(self):

        self.viewer.add_data(self.image1)

        x_min_start = self.viewer.state.x_min
        x_max_start = self.viewer.state.x_max

        self.options_widget.button_flip_x.click()

        assert self.viewer.state.x_min == x_max_start
        assert self.viewer.state.x_max == x_min_start

        y_min_start = self.viewer.state.y_min
        y_max_start = self.viewer.state.y_max

        self.options_widget.button_flip_y.click()

        assert self.viewer.state.y_min == y_max_start
        assert self.viewer.state.y_max == y_min_start

    def test_combo_updates_with_component_add(self):
        self.viewer.add_data(self.image1)
        self.image1.add_component([[9, 9], [8, 8]], 'z')
        assert self.viewer.state.x_att_world is self.image1.id['World 1']
        assert self.viewer.state.y_att_world is self.image1.id['World 0']
        # TODO: there should be an easier way to do this
        layer_style_editor = self.viewer._view.layout_style_widgets[self.viewer.layers[0]]
        assert combo_as_string(layer_style_editor.ui.combodata_attribute) == 'x:y:z'

    def test_apply_roi(self):

        self.viewer.add_data(self.image1)

        roi = RectangularROI(0.4, 1.6, -0.6, 0.6)

        assert len(self.viewer.layers) == 1

        self.viewer.apply_roi(roi)

        assert len(self.viewer.layers) == 2
        assert len(self.image1.subsets) == 1

        assert_allclose(self.image1.subsets[0].to_mask(), [[0, 1], [0, 0]])

        state = self.image1.subsets[0].subset_state
        assert isinstance(state, RoiSubsetState)

    def test_identical(self):

        # Check what happens if we set both attributes to the same coordinates

        self.viewer.add_data(self.image2)

        assert self.viewer.state.x_att_world is self.image2.id['Apple']
        assert self.viewer.state.y_att_world is self.image2.id['Banana']

        self.viewer.state.y_att_world = self.image2.id['Apple']

        assert self.viewer.state.x_att_world is self.image2.id['Banana']
        assert self.viewer.state.y_att_world is self.image2.id['Apple']

        self.viewer.state.x_att_world = self.image2.id['Apple']

        assert self.viewer.state.x_att_world is self.image2.id['Apple']
        assert self.viewer.state.y_att_world is self.image2.id['Banana']

    def test_duplicate_subsets(self):

        # Regression test: make sure that when adding a seconda layer for the
        # same dataset, we don't add the subsets all over again.

        self.viewer.add_data(self.image1)
        self.data_collection.new_subset_group(subset_state=self.image1.id['x'] > 1, label='A')

        assert len(self.viewer.layers) == 2

        self.viewer.add_data(self.image1)

        assert len(self.viewer.layers) == 3

    def test_aspect_subset(self):

        self.viewer.add_data(self.image1)

        assert self.viewer.state.aspect == 'equal'
        assert self.viewer.axes.get_aspect() == 'equal'

        self.viewer.state.aspect = 'auto'

        self.data_collection.new_subset_group('s1', self.image1.id['x'] > 0.)

        assert len(self.viewer.state.layers) == 2

        assert self.viewer.state.aspect == 'auto'
        assert self.viewer.axes.get_aspect() == 'auto'

        self.viewer.state.aspect = 'equal'

        self.data_collection.new_subset_group('s2', self.image1.id['x'] > 1.)

        assert len(self.viewer.state.layers) == 3

        assert self.viewer.state.aspect == 'equal'
        assert self.viewer.axes.get_aspect() == 'equal'

    def test_hypercube(self):

        # Check defaults when we add data

        self.viewer.add_data(self.hypercube)

        assert combo_as_string(self.options_widget.ui.combosel_x_att_world) == 'World 0:World 1:World 2:World 3'
        assert combo_as_string(self.options_widget.ui.combosel_x_att_world) == 'World 0:World 1:World 2:World 3'

        assert self.viewer.axes.get_xlabel() == 'World 3'
        assert self.viewer.state.x_att_world is self.hypercube.id['World 3']
        assert self.viewer.state.x_att is self.hypercube.pixel_component_ids[3]
        # TODO: make sure limits are deterministic then update this
        # assert self.viewer.state.x_min == -0.5
        # assert self.viewer.state.x_max == +1.5

        assert self.viewer.axes.get_ylabel() == 'World 2'
        assert self.viewer.state.y_att_world is self.hypercube.id['World 2']
        assert self.viewer.state.y_att is self.hypercube.pixel_component_ids[2]
        # TODO: make sure limits are deterministic then update this
        # assert self.viewer.state.y_min == -0.5
        # assert self.viewer.state.y_max == +1.5

        assert not self.viewer.state.x_log
        assert not self.viewer.state.y_log

        assert len(self.viewer.state.layers) == 1

    def test_hypercube_world(self):

        # Check defaults when we add data

        wcs = WCS(naxis=4)
        hypercube2 = Data()
        hypercube2.coords = WCSCoordinates(wcs=wcs)
        hypercube2.add_component(np.random.random((2, 3, 4, 5)), 'a')

        self.data_collection.append(hypercube2)

        self.viewer.add_data(hypercube2)

    def test_incompatible_subset(self):
        self.viewer.add_data(self.image1)
        self.data_collection.new_subset_group(subset_state=self.catalog.id['c'] > 1, label='A')

    def test_apply_roi_single(self):

        # Regression test for a bug that caused mode.update to be called
        # multiple times and resulted in all other viewers receiving many
        # messages regarding subset updates (this occurred when multiple)
        # datasets were present.

        layer_tree = LayerTreeWidget()
        layer_tree.set_checkable(False)
        layer_tree.setup(self.data_collection)
        layer_tree.bind_selection_to_edit_subset()

        class Client(HubListener):

            def __init__(self, *args, **kwargs):
                super(Client, self).__init__(*args, **kwargs)
                self.count = Counter()

            def ping(self, message):
                self.count[message.sender] += 1

            def register_to_hub(self, hub):
                hub.subscribe(self, SubsetUpdateMessage, handler=self.ping)

        d1 = Data(a=[[1, 2], [3, 4]], label='d1')
        d2 = Data(b=[[1, 2], [3, 4]], label='d2')
        d3 = Data(c=[[1, 2], [3, 4]], label='d3')
        d4 = Data(d=[[1, 2], [3, 4]], label='d4')

        self.data_collection.append(d1)
        self.data_collection.append(d2)
        self.data_collection.append(d3)
        self.data_collection.append(d4)

        client = Client()
        client.register_to_hub(self.hub)

        self.viewer.add_data(d1)
        self.viewer.add_data(d3)

        roi = XRangeROI(2.5, 3.5)
        self.viewer.apply_roi(roi)

        for subset in client.count:
            assert client.count[subset] == 1

    def test_disable_incompatible(self):

        # Test to make sure that image and image subset layers are disabled if
        # their pixel coordinates are not compatible with the ones of the
        # reference data.

        self.viewer.add_data(self.image1)
        self.viewer.add_data(self.image2)

        assert self.viewer.state.reference_data is self.image1

        self.data_collection.new_subset_group()

        assert len(self.viewer.layers) == 4

        # Only the two layers associated with the reference data should be enabled
        for layer_artist in self.viewer.layers:
            if layer_artist.layer in (self.image1, self.image1.subsets[0]):
                assert layer_artist.enabled
            else:
                assert not layer_artist.enabled

        py1, px1 = self.image1.pixel_component_ids
        py2, px2 = self.image2.pixel_component_ids

        link1 = LinkSame(px1, px2)
        self.data_collection.add_link(link1)

        # One link isn't enough, second dataset layers are still not enabled

        for layer_artist in self.viewer.layers:
            if layer_artist.layer in (self.image1, self.image1.subsets[0]):
                assert layer_artist.enabled
            else:
                assert not layer_artist.enabled

        link2 = LinkSame(py1, py2)
        self.data_collection.add_link(link2)

        # All layers should now be enabled

        for layer_artist in self.viewer.layers:
            assert layer_artist.enabled

        self.data_collection.remove_link(link2)

        # We should now be back to the original situation

        for layer_artist in self.viewer.layers:
            if layer_artist.layer in (self.image1, self.image1.subsets[0]):
                assert layer_artist.enabled
            else:
                assert not layer_artist.enabled

    def test_change_reference_data(self, capsys):

        # Test to make sure everything works fine if we change the reference data.

        self.viewer.add_data(self.image1)
        self.viewer.add_data(self.image2)

        assert self.viewer.state.reference_data is self.image1
        assert self.viewer.state.x_att_world is self.image1.world_component_ids[-1]
        assert self.viewer.state.y_att_world is self.image1.world_component_ids[-2]
        assert self.viewer.state.x_att is self.image1.pixel_component_ids[-1]
        assert self.viewer.state.y_att is self.image1.pixel_component_ids[-2]

        self.viewer.state.reference_data = self.image2

        assert self.viewer.state.reference_data is self.image2
        assert self.viewer.state.x_att_world is self.image2.world_component_ids[-1]
        assert self.viewer.state.y_att_world is self.image2.world_component_ids[-2]
        assert self.viewer.state.x_att is self.image2.pixel_component_ids[-1]
        assert self.viewer.state.y_att is self.image2.pixel_component_ids[-2]

        self.viewer.state.reference_data = self.image1

        assert self.viewer.state.reference_data is self.image1
        assert self.viewer.state.x_att_world is self.image1.world_component_ids[-1]
        assert self.viewer.state.y_att_world is self.image1.world_component_ids[-2]
        assert self.viewer.state.x_att is self.image1.pixel_component_ids[-1]
        assert self.viewer.state.y_att is self.image1.pixel_component_ids[-2]

        # Some exceptions used to happen during callbacks, and these show up
        # in stderr but don't interrupt the code, so we make sure here that
        # nothing was printed to stdout nor stderr.

        out, err = capsys.readouterr()

        assert out.strip() == ""
        assert err.strip() == ""

    @pytest.mark.parametrize('wcs', [False, True])
    def test_change_reference_data_dimensionality(self, capsys, wcs):

        # Regression test for a bug that caused an exception when changing
        # the dimensionality of the reference data

        if wcs:
            first = self.image1_wcs
            second = self.hypercube_wcs
        else:
            first = self.image1
            second = self.hypercube

        self.viewer.add_data(first)
        self.viewer.add_data(second)

        assert self.viewer.state.reference_data is first
        assert self.viewer.state.x_att_world is first.world_component_ids[-1]
        assert self.viewer.state.y_att_world is first.world_component_ids[-2]
        assert self.viewer.state.x_att is first.pixel_component_ids[-1]
        assert self.viewer.state.y_att is first.pixel_component_ids[-2]

        self.viewer.state.reference_data = second

        assert self.viewer.state.reference_data is second
        assert self.viewer.state.x_att_world is second.world_component_ids[-1]
        assert self.viewer.state.y_att_world is second.world_component_ids[-2]
        assert self.viewer.state.x_att is second.pixel_component_ids[-1]
        assert self.viewer.state.y_att is second.pixel_component_ids[-2]

        self.viewer.state.reference_data = first

        assert self.viewer.state.reference_data is first
        assert self.viewer.state.x_att_world is first.world_component_ids[-1]
        assert self.viewer.state.y_att_world is first.world_component_ids[-2]
        assert self.viewer.state.x_att is first.pixel_component_ids[-1]
        assert self.viewer.state.y_att is first.pixel_component_ids[-2]

        # Some exceptions used to happen during callbacks, and these show up
        # in stderr but don't interrupt the code, so we make sure here that
        # nothing was printed to stdout nor stderr.

        out, err = capsys.readouterr()

        assert out.strip() == ""
        assert err.strip() == ""

    def test_scatter_overlay(self):
        self.viewer.add_data(self.image1)
        self.viewer.add_data(self.catalog)


class TestSessions(object):

    @pytest.mark.parametrize('protocol', [0, 1])
    def test_session_back_compat(self, protocol):

        filename = os.path.join(DATA, 'image_v{0}.glu'.format(protocol))

        with open(filename, 'r') as f:
            session = f.read()

        state = GlueUnSerializer.loads(session)

        ga = state.object('__main__')

        dc = ga.session.data_collection

        assert len(dc) == 2

        assert dc[0].label == 'data1'
        assert dc[1].label == 'data2'

        viewer1 = ga.viewers[0][0]

        assert len(viewer1.state.layers) == 3

        assert viewer1.state.x_att_world is dc[0].id['World 1']
        assert viewer1.state.y_att_world is dc[0].id['World 0']

        assert viewer1.state.x_min < -0.5
        assert viewer1.state.x_max > 1.5
        assert viewer1.state.y_min <= -0.5
        assert viewer1.state.y_max >= 1.5

        layer_state = viewer1.state.layers[0]
        assert isinstance(layer_state, ImageLayerState)
        assert layer_state.visible
        assert layer_state.bias == 0.5
        assert layer_state.contrast == 1.0
        assert layer_state.stretch == 'sqrt'
        assert layer_state.percentile == 99

        layer_state = viewer1.state.layers[1]
        assert isinstance(layer_state, ScatterLayerState)
        assert layer_state.visible

        layer_state = viewer1.state.layers[2]
        assert isinstance(layer_state, ImageSubsetLayerState)
        assert not layer_state.visible

        viewer2 = ga.viewers[0][1]

        assert len(viewer2.state.layers) == 2

        assert viewer2.state.x_att_world is dc[0].id['World 1']
        assert viewer2.state.y_att_world is dc[0].id['World 0']

        assert viewer2.state.x_min < -0.5
        assert viewer2.state.x_max > 1.5
        assert viewer2.state.y_min <= -0.5
        assert viewer2.state.y_max >= 1.5

        layer_state = viewer2.state.layers[0]
        assert layer_state.visible
        assert layer_state.stretch == 'arcsinh'
        assert layer_state.v_min == 1
        assert layer_state.v_max == 4

        layer_state = viewer2.state.layers[1]
        assert layer_state.visible

        viewer3 = ga.viewers[0][2]

        assert len(viewer3.state.layers) == 2

        assert viewer3.state.x_att_world is dc[0].id['World 1']
        assert viewer3.state.y_att_world is dc[0].id['World 0']

        assert viewer3.state.x_min < -0.5
        assert viewer3.state.x_max > 1.5
        assert viewer3.state.y_min <= -0.5
        assert viewer3.state.y_max >= 1.5

        layer_state = viewer3.state.layers[0]
        assert layer_state.visible
        assert layer_state.stretch == 'linear'
        assert layer_state.v_min == -2
        assert layer_state.v_max == 2

        layer_state = viewer3.state.layers[1]
        assert layer_state.visible

    @pytest.mark.parametrize('protocol', [0, 1])
    def test_session_cube_back_compat(self, protocol):

        filename = os.path.join(DATA, 'image_cube_v{0}.glu'.format(protocol))

        with open(filename, 'r') as f:
            session = f.read()

        state = GlueUnSerializer.loads(session)

        ga = state.object('__main__')

        dc = ga.session.data_collection

        assert len(dc) == 1

        assert dc[0].label == 'array'

        viewer1 = ga.viewers[0][0]

        assert len(viewer1.state.layers) == 1

        assert viewer1.state.x_att_world is dc[0].id['World 2']
        assert viewer1.state.y_att_world is dc[0].id['World 1']
        assert viewer1.state.slices == [2, 0, 0, 1]

    @pytest.mark.parametrize('protocol', [0, 1])
    def test_session_rgb_back_compat(self, protocol):

        filename = os.path.join(DATA, 'image_rgb_v{0}.glu'.format(protocol))

        with open(filename, 'r') as f:
            session = f.read()

        state = GlueUnSerializer.loads(session)

        ga = state.object('__main__')

        dc = ga.session.data_collection

        assert len(dc) == 1

        assert dc[0].label == 'rgbcube'

        viewer1 = ga.viewers[0][0]

        assert len(viewer1.state.layers) == 3
        assert viewer1.state.color_mode == 'One color per layer'

        layer_state = viewer1.state.layers[0]
        assert layer_state.visible
        assert layer_state.attribute.label == 'a'
        assert layer_state.color == 'r'

        layer_state = viewer1.state.layers[1]
        assert not layer_state.visible
        assert layer_state.attribute.label == 'c'
        assert layer_state.color == 'g'

        layer_state = viewer1.state.layers[2]
        assert layer_state.visible
        assert layer_state.attribute.label == 'b'
        assert layer_state.color == 'b'
