# -*- coding: utf-8 -*-

# Copyright (c) 2011-2017, Camptocamp SA
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.

import logging
from json import dumps, loads

from c2cgeoportal.lib.filter_capabilities import get_protected_layers, \
    get_private_layers

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPForbidden, HTTPBadRequest

from c2cgeoportal.lib.caching import NO_CACHE
from c2cgeoportal.views.proxy import Proxy

log = logging.getLogger(__name__)


class PdfReport(Proxy):  # pragma: no cover

    layername = None

    def __init__(self, request):
        Proxy.__init__(self, request)
        self.config = self.request.registry.settings.get("pdfreport", {})

    def _do_print(self, spec):
        """ Create and get report PDF. """

        headers = dict(self.request.headers)
        headers["Content-Type"] = "application/json"
        resp, content = self._proxy(
            "{0!s}/buildreport.{1!s}".format(
                self.config["print_url"],
                spec["outputFormat"]
            ),
            method="POST",
            body=dumps(spec),
            headers=headers
        )

        return self._build_response(
            resp, content, NO_CACHE, "pdfreport",
        )

    @staticmethod
    def _build_map(mapserv_url, vector_request_url, srs, map_config):
        backgroundlayers = map_config["backgroundlayers"]
        imageformat = map_config["imageformat"]
        return {
            "projection": srs,
            "dpi": 254,
            "rotation": 0,
            "bbox": [0, 0, 1000000, 1000000],
            "zoomToFeatures": {
                "zoomType": map_config["zoomType"],
                "layer": "vector",
                "minScale": map_config["minScale"],
            },
            "layers": [{
                "type": "gml",
                "name": "vector",
                "style": {
                    "version": "2",
                    "[1 > 0]": map_config["style"]
                },
                "opacity": 1,
                "url": vector_request_url
            }, {
                "baseURL": mapserv_url,
                "opacity": 1,
                "type": "WMS",
                "serverType": "mapserver",
                "layers": backgroundlayers,
                "imageFormat": imageformat
            }]
        }

    @view_config(route_name="pdfreport", renderer="json")
    def get_report(self):
        id_ = self.request.matchdict["id"]
        self.layername = self.request.matchdict["layername"]
        layer_config = self.config["layers"].get(self.layername)

        if layer_config is None:
            raise HTTPBadRequest("Layer not found")

        if layer_config["check_credentials"]:
            # check user credentials
            role_id = None if self.request.user is None else \
                self.request.user.role.id

            # FIXME: support of mapserver groups
            if self.layername in get_private_layers() and \
                    self.layername not in get_protected_layers(role_id):
                raise HTTPForbidden

        srs = layer_config["srs"]

        mapserv_url = self.request.route_url("mapserverproxy")
        vector_request_url = "{0!s}?{1!s}".format(
            mapserv_url,
            "&".join(["{0!s}={1!s}".format(*i) for i in {
                "service": "WFS",
                "version": "1.1.0",
                "outputformat": "gml3",
                "request": "GetFeature",
                "typeName": self.layername,
                "featureid": self.layername + "." + id_,
                "srsName": "epsg:" + str(srs)
            }.items()])
        )

        spec = layer_config["spec"]
        if spec is None:
            spec = {
                "layout": self.layername,
                "outputFormat": "pdf",
                "attributes": {
                    "paramID": id_
                }
            }
            map_config = layer_config.get("map")
            if map_config is not None:
                spec["attributes"]["map"] = self._build_map(
                    mapserv_url, vector_request_url, srs, map_config
                )

            maps_config = layer_config.get("maps")
            if maps_config is not None:
                spec["attributes"]["maps"] = []
                for map_config in maps_config:
                    spec["attributes"]["maps"].append(self._build_map(
                        mapserv_url, vector_request_url, srs, map_config
                    ))
        else:
            spec = loads(dumps(spec) % {
                "layername": self.layername,
                "id": id_,
                "srs": srs,
                "mapserv_url": mapserv_url,
                "vector_request_url": vector_request_url,
            })

        return self._do_print(spec)
