import os
import json
import traceback
import glob
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
from sklearn.decomposition import PCA

model = ResNet50(weights='imagenet')
vectors = []
filenames = []

def _do_pca():
    if len(vectors) > 1:
        pca = PCA(n_components=2)
        X = pca.fit_transform(np.array(vectors))
        return JsonResponse({"filenames": filenames, "vectors": X.tolist()}, safe=False)
    else:
        return JsonResponse({"filenames": filenames, "vectors": []}, safe=False)

@require_http_methods(["GET"])
def index(request):
    return render(request, 'index.html')

@require_http_methods(["POST"])
def get_vector(request):
    try:
        uploadedFile = request.FILES['myfile'] if 'myfile' in request.FILES else False
        if uploadedFile:
            fss = FileSystemStorage()
            filename = fss.save(uploadedFile.name, uploadedFile)
            print(filename)

            img = image.load_img(os.path.join(settings.MEDIA_ROOT, filename), target_size=(224, 224))
            
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            preds = model.predict(x)
            
            filenames.append(filename)
            vectors.append(preds[0])
            
            return _do_pca()
        else:
            return JsonResponse({"msg": "file not exist"}, safe=False, status=400)
    except:
        print(traceback.format_exc())
        return JsonResponse({"msg": "Exception thrown"}, safe=False, status=500)

@require_http_methods(["GET"])
def get_pca(request):
    global vectors
    global filenames

    try:
        tmp = []
        fn = []
        types = (f"{settings.MEDIA_ROOT}/*.jpg", f"{settings.MEDIA_ROOT}/*.png", f"{settings.MEDIA_ROOT}/*.jpeg") 
        files_grabbed = []
        for t in types:
            files_grabbed.extend(glob.glob(t))

        for fp in files_grabbed:
            print(fp)
            img = image.load_img(fp, target_size=(224, 224))
            
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            preds = model.predict(x)
            
            filename, file_extension =os.path.splitext(os.path.basename(fp))
            
            fn.append(filename + file_extension)
            tmp.append(preds[0])
    
        vectors = tmp
        filenames = fn

        return _do_pca()
    except:
        print(traceback.format_exc())
        return JsonResponse({"msg": "Exception thrown"}, safe=False, status=500)


@require_http_methods(["GET"])
def get_file(request):
    try:
        return JsonResponse({"msg": "file not exist"}, safe=False, status=400)
    except:
        print(traceback.format_exc())
        return JsonResponse({"msg": "Exception thrown"}, safe=False, status=500)

