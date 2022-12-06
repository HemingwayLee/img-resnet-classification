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
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
# from matplotlib.font_manager import FontProperties
# from sklearn.decomposition import PCA
# import matplotlib.pyplot as plt
import numpy as np

model = ResNet50(weights='imagenet')

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
            
            # # image.array_to_img(img).show()

            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            preds = model.predict(x)
            print(preds)
            # # print('Predicted:', decode_predictions(preds, top=3)[0])

            # filename, _ =os.path.splitext(os.path.basename(fp))
            # print(filename)

            return JsonResponse({"name": filename, "vector": preds.tolist()}, safe=False)
    except:
        print(traceback.format_exc())
        return JsonResponse({"msg": "Exception thrown"}, safe=False, status=500)
