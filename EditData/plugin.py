import climmob.plugins as plugins
import climmob.plugins.utilities as u
import climmob.resources as r
from views import myPublicView,myPrivateView



class EditData(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IConfig)
    plugins.implements(plugins.IResource)
    plugins.implements(plugins.ISchema)

    def before_mapping(self, config):
        #We don't add any routes before the host application
        return []

    def after_mapping(self, config):
        #We add here a new route /json that returns a JSON
        custom_map = []
        custom_map.append(u.addRoute('mypublicview','/mypublicview',myPublicView,'public.jinja2'))
        custom_map.append(u.addRoute('myprivateview', '/myprivateview', myPrivateView, 'private.jinja2'))
        return custom_map

    def update_config(self, config):
        #We add here the templates of the plugin to the config
        u.addTemplatesDirectory(config,'templates')


    def add_libraries(self, config):
        # We add here our new library using the fanstatic directory of the plugin
        libraries = []
        libraries.append(u.addLibrary('plibrary', 'fanstatic'))
        return libraries


    def add_JSResources(self, config, loadedJSResources):
        # We add here two new JavaScripts: leaflet and mymap.js so we can required then later on in mytemplate.jinja2
        # The JS of leaflet required bootstrap so it will be included after the JS of bootstrap
        # My map requires leaflet so if we need mymap it will include the JS of leaflet
        myJS = []
        #myJS.append(u.addJSResource('coreresources', 'footable', 'inspinia/js/plugins/footable/footable.all.min.js','slimscroll'))
        myJS.append(u.addJSResource('coreresources', 'gridl', 'inspinia/js/plugins/jqGrid/i18n/grid.locale-en.js','slimscroll'))
        myJS.append(u.addJSResource('coreresources', 'jqgrid', 'inspinia/js/plugins/jqGrid/jquery.jqGrid.min.js','slimscroll'))
        myJS.append(u.addJSResource('coreresources', 'sweet', 'inspinia/js/plugins/sweetalert/sweetalert.min.js', 'slimscroll'))

        myJS.append(u.addJSResource('plibrary', 'editDatajq', 'editData_jqgrid.js', 'slimscroll'))



        return myJS


    def add_CSSResources(self, config, loadedCSSResources):
        # We add here the new css for leaflet we can required it later on in mytemplate.jinja2
        myCSS = []
        #myCSS.append(u.addCSSResource('coreresources', 'footable', 'inspinia/css/plugins/footable/footable.core.css', 'fontawesome'))

        #myCSS.append(u.addCSSResource('coreresources', 'jquery', 'inspinia/css/plugins/jQueryUI/jquery-ui-1.10.4.custom.min.css', 'fontawesome'))
        myCSS.append(u.addCSSResource('coreresources', 'jqgrid', 'inspinia/css/plugins/jqGrid/ui.jqgrid.css', 'jqueryui'))
        myCSS.append(u.addCSSResource('coreresources', 'sweet', 'inspinia/css/plugins/sweetalert/sweetalert.css', 'jqgrid'))

        return myCSS

    def update_schema(self, config):
        myfields = []
        #myfields.append(u.addFieldToProjectSchema("fecha", "Fecha del pueblo"))
        return myfields