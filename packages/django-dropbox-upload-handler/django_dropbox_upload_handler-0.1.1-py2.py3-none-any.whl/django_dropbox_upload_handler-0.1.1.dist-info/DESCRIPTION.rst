=============================
Django Dropbox Upload Handler
=============================

.. image:: https://badge.fury.io/py/django-dropbox-upload-handler.svg
    :target: https://badge.fury.io/py/django-dropbox-upload-handler

.. image:: https://travis-ci.org/jagonalez/django-dropbox-upload-handler.svg?branch=master
    :target: https://travis-ci.org/jagonalez/django-dropbox-upload-handler

.. image:: https://codecov.io/gh/jagonalez/django-dropbox-upload-handler/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jagonalez/django-dropbox-upload-handler

Transfer Uploaded Files to Dropbox

Quickstart
----------

Install Django Dropbox Upload Handler::

    pip install django-dropbox-upload-handler

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_dropbox_upload_handler.apps.DjangoDropboxUploadHandlerConfig',
        ...
    )

Add DropboxFileUploadHandler to the default Upload Handlers:

.. code-block:: python

    FILE_UPLOAD_HANDLERS = [
        'django_dropbox_upload_handler.handler.DropboxFileUploadHandler'
    ]

To Enable DropboxFileUploadHandler within a single view:

forms.py

.. code-block:: python

    from django import forms

    class UploadFileForm(forms.Form):
      title = forms.CharField(max_length=50)
      file = forms.FileField()


views.py

.. code-block:: python

    from django.http import HttpResponseRedirect
    from django.shortcuts import render
    from .forms import UploadFileForm

    # Imaginary function to handle the uploaded file dropbox file.
    from somewhere import handle_uploaded_file

    def upload_file(request):
        if request.method == 'POST':
            self.request.upload_handlers.insert(0, DropboxFileUploadHandler(request))
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
                return HttpResponseRedirect('/success/url/')
        else:
            form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})


Add Django Dropbox Upload Handler's URL patterns:

.. code-block:: python

    from django_dropbox_upload_handler import urls as django_dropbox_upload_handler_urls


    urlpatterns = [
        ...
        url(r'^', include(django_dropbox_upload_handler_urls)),
        ...
    ]

Checking upload progress for API:

When submitting the file include the parameter progres_id in the URL. ex:

.. code-block:: javascript

    function getUUID() {
      let uuid = ""
      for (let i=0; i < 32; i++) {
        uuid += Math.floor(Math.random() * 16).toString(16);
      }
      return uuid
    }

    function upload(file) {
      let data = new FormData()
      data.append('file', file)
      fetch('/path/to/upload?progress_id=' + getUUID(), {
        method: "post",
        body: data
      })
      .then(response => {
        //...
      })
      checkProgress(0, progressId, file.size)
    }

    function checkProgress(progressId, size) {
      fetch('/upload_progress?progress_id=' = progiressId)
      .then(response => {
        if (r.status === 201)
          return {done: 'true'}
        return response.json()
      })
      .then(data => {
        if (data.done) {
          //..upload is completed
        } else {
          //.. still uploading - progress can be checked using:
          progress = Math.round(parseInt(data.uploaded) / parseInt(data.length) * 100)
          setTimeout(() => { checkProgress( progressId, size) }, 500)
        }
      })
    }

Features
--------

* Transfers files uploaded through Django to Dropbox
* Includes a upload_progress view for ajax calls

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------

0.1.0 (2017-09-03)
++++++++++++++++++

* First release on PyPI.


