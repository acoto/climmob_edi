import climmob.plugins.utilities as u
from climmob.plugins.utilities import climmobPublicView, climmobPrivateView

from edit_data import getNamesEditByColums, fillDataTable, update_edited_data


class myPublicView(climmobPublicView):
    def processView(self):
        return {}


class myPrivateView(climmobPrivateView):
    def processView(self):

        proId = 'www'  # the name of project or database in edit module, www is the test database
        #u.getJSResource('jquery').need()
        u.getJSResource('bootstrap').need()
        u.getJSResource('qlibrary').need()

        # edit by columns code
        u.getJSResource('icheck').need()
        u.getCSSResource('icheck').need()
        u.getJSResource('editDatajq').need()

        u.getCSSResource('select2').need()
        u.getJSResource('select2').need()

        dataworking = {}  #
        dataworking['error'] = ''
        dataworking['data'] = False

        if 'btn_EditData' in self.request.POST:
            selected_contacts = self.request.POST.getall("q_reg")
            if len(selected_contacts) == 0:  # if non selected columns in check options

                dataworking['error'] = 'byC'
                dataworking['msg'] = True
            else:  # if the user select more than 1 columns
                u.getJSResource('gridl').need()
                u.getJSResource('jqgrid').need()
                u.getJSResource('sweet').need()

                u.getCSSResource('jqgrid').need()
                #u.getCSSResource('jquery').need()
                u.getCSSResource('sweet').need()

                dataworking['data'] = True
                dataworking['fill'] = fillDataTable(self, proId, selected_contacts)
                dataworking['error'] = ''
        else:
            if 'json_data' in self.request.POST:
                json_data = self.request.POST.getall("json_data")
                dataworking['error'] = 'byC'
                dataworking['data'] = False
                dataworking['msg'] = False
                u.getJSResource('sweet').need()
                u.getCSSResource('sweet').need()
                if json_data[0] != '':
                    dataworking['msg_flag'] = update_edited_data(self, proId, json_data)

        return {'dataworking': dataworking, 'activeUser': self.user, 'getNamesEditByColums': getNamesEditByColums(proId,
                                                                                                                  self.request.registry.settings[
                                                                                                                      'user.repository'])}  # 'fill_table_n': fill_table_n(self,proId),
