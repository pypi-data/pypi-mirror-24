from zipstream import ZipFile, ZIP_DEFLATED

from django.views.generic.detail import BaseDetailView
from django.utils.translation import activate
from django.http import StreamingHttpResponse
from django.conf import settings

from relatorio.templates.opendocument import Template

from .models import Document
from .utils import StringIterator


class BaseDocumentFileView(BaseDetailView):

    model = Document

    def get_object_name(self, obj=None, obj_id=None):

        assert obj_id is not None or obj is not None, 'You need to provide either an obj or an obj_id'

        if obj is None:
            obj = self.get_target(self.get_object(), obj_id)

        if hasattr(obj, 'print_str'):
          return obj.print_str()
        return '{}'.format(obj.pk)

    def get_target(self, document, obj_id):
        klass = document.content_type.model_class()
        return klass.objects.get(pk=obj_id)

    def get_file(self, document, obj_id=None, obj=None):
        document.source.open()

        assert obj_id is not None or obj is not None, 'You need to provide either an obj or an obj_id'

        if obj is None:
            obj = self.get_target(document, obj_id)
        else:
            obj_id = obj.id

        object_name = self.get_object_name(obj)

        if document.get_language_from_target and hasattr(obj, 'output_lang') and obj.output_lang(self.request):
          activate(obj.output_lang(self.request))

        tpl = Template(source=None, filepath=document.source)
        generated = tpl.generate(o=obj).render()

        extension = document.extension
        if document.convert_to is None or document.convert_to == '':
          output = generated.getvalue()

        else:
          import subprocess
          import shlex
          import tempfile
          import os

          input = tempfile.NamedTemporaryFile(delete=False)
          input.write(generated.getvalue())
          input.close()

          command_line = '/usr/bin/loffice --headless --convert-to {} --outdir {} {}'.format(
              extension,
              os.path.dirname(input.name),
              input.name
          )
          subprocess.call(shlex.split(command_line))

          output_filename = '{}.{}'.format(input.name, extension)
          if document.merge_with_tos and extension == 'pdf':
            final_name = os.path.join('/tmp', '{}_{}.{}'.format(document.name, object_name, extension))
            command_line = 'pdfunite {} {} {}'.format(output_filename, settings.TOS_FILE, final_name)
            print(command_line)
            subprocess.call(shlex.split(command_line))
            os.unlink(output_filename)
            output_filename = final_name

          output_stream = open(output_filename, 'rb')
          output = output_stream.read()
          os.unlink(input.name)
          os.unlink(output_filename)

        return output


class DocumentFileView(BaseDocumentFileView):

    def get(self, request, *args, **kwargs):

        document = self.get_object()
        obj_id = kwargs.get('object_id')
        obj = self.get_target(document, obj_id)

        rv = StreamingHttpResponse(StringIterator(obj_id, document, self), content_type=document.output_type)
        rv['Content-Disposition'] = 'attachment; filename={}_{}.{}'.format(
            document.name,
            self.get_object_name(obj),
            document.extension
        )

        return rv


class BulkDocumentFileView(BaseDocumentFileView):

    def get_object_ids(self):
        return self.request.GET.getlist('ids[]', [])

    def get_zip(self, request, document):
        zipstream = ZipFile(compress=ZIP_DEFLATED)
        for id in self.get_object_ids():
            zipstream.write_iter(
                '{}_{}.{}'.format(document.name, self.get_object_name(id), document.extension),
                StringIterator(document, id, self)
            )
        return zipstream

    def get(self, request, *args, **kwargs):
        document = self.get_object()

        rv = StreamingHttpResponse(self.get_zip(request, document), content_type='application/zip')
        rv['Content-Disposition'] = 'attachment; filename={}.zip'.format(document.name)

        return rv
