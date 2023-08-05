# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import Products.JWPlayer


class ProductsJwplayerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=Products.JWPlayer)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.JWPlayer:default')


PRODUCTS_JWPLAYER_FIXTURE = ProductsJwplayerLayer()


PRODUCTS_JWPLAYER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PRODUCTS_JWPLAYER_FIXTURE,),
    name='ProductsJwplayerLayer:IntegrationTesting'
)


PRODUCTS_JWPLAYER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PRODUCTS_JWPLAYER_FIXTURE,),
    name='ProductsJwplayerLayer:FunctionalTesting'
)


PRODUCTS_JWPLAYER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PRODUCTS_JWPLAYER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='ProductsJwplayerLayer:AcceptanceTesting'
)
