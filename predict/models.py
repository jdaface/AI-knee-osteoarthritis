from django.db import models
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.utils.translation import ugettext_lazy as _
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing. image import load_img, img_to_array
from tensorflow.keras.models import load_model, model_from_json
from keras.initializers import glorot_uniform
from keras.utils import CustomObjectScope
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.optimizers import Adam
from keras.losses import categorical_crossentropy
from tensorflow.keras import backend as K

from users.models import Patient, Doctor
# Create your models here.


class Classification(models.Model):
    img = models.ImageField(_("X-ray images"), upload_to='media')

    prediction = models.CharField(_("Prediction"), max_length=500, blank=True)

    def predict_koa(self):
        K.reset_uids()

        model = "models\model.json"
        weights = "models/model_weight.h5"
        classes = {
            'TRAIN': ['GRADE 0', 'GRADE 1', 'GRADE 2', 'GRADE 3', 'GRADE 4'],
            'VALIDATION': ['GRADE 0', 'GRADE 1', 'GRADE 2', 'GRADE 3', 'GRADE 4'],
            'TEST': ['GRADE 0', 'GRADE 1', 'GRADE 2', 'GRADE 3', 'GRADE 4'],
        }
        with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
            with open(model, 'r') as f:
                model = model_from_json(f.read())
                model.load_weights(weights)

        img = image.load_img(self.img, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        model.compile(loss="categorical_crossentropy", metrics=[
                      "accuracy"], optimizer="adam")
        result = model.predict(x)
        

        pred_name = classes['TRAIN'][np.argmax(result)]

        
        print("The osteoarthritis is classified to be {}.".format(pred_name))
        
        return pred_name

    def save(self, *args, **kwargs):
        self.prediction = self.predict_koa()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('list')



