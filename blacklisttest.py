import json
import time
from flask import Response
from flask_jwt_extended import create_access_token
from datetime import timedelta

from unittest import TestCase
from unittest.mock import Mock, patch
import uuid 

from application import application

class testBlackList(TestCase):

    def setUp(self):
        self.client=application.test_client()
        self.tokenfijo="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MDYyMzQwNCwianRpIjoiZmVjYTI5NTAtY2I1My00ZWVkLWFiN2ItZjM5ZTMwMDg2NzkxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjgwNjIzNDA0fQ.aF924YU7GlLR_u6YuFZeZgul2o75ltDYrNkIC6e4a4Q"
        self.userId=2
        self.offerId=1
        self.postId=1
        access_token_expires = timedelta(minutes=120)
        self.token=create_access_token(identity=self.userId, expires_delta=access_token_expires)
        access_token_expires = timedelta(seconds=3)
        self.tokenexpired=create_access_token(identity=self.userId, expires_delta=access_token_expires)
        #self.token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NTczMTY3MywianRpIjoiOGU1OWJjZmQtNTJlYi00YzQ1LWI1NDUtZTU3MGYxMDBiNTQ0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjc1NzMxNjczLCJleHAiOjE2NzU3Mzg4NzN9.iPaNwx0Sp2TcPOyv5p12e7RyPAUDih3lrLxV0mVN43Q"
        #self.tokenexpired="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NTY4NDg3NiwianRpIjoiZjdkYzNlN2QtMzFhNy00NWZhLTg3NjItNzIwZDQ0NTUyMWZjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjc1Njg0ODc2LCJleHAiOjE2NzU2ODY2NzZ9.fPQFhAK_4k16NqpMGcT2eV-q-PQRUKHrLMiQY-xzDYM"

    def test_raiz(self):
        endpoint_raiz='/'
        solicitud_raiz=self.client.get(endpoint_raiz)
        respuesta_raiz=json.loads(solicitud_raiz.get_data())
        msg=respuesta_raiz["Mensaje"]
        self.assertEqual(solicitud_raiz.status_code, 200)
        self.assertIn("Hola", msg)

    def test_ping(self):
        endpoint_ping='/ping'
        solicitud_ping=self.client.get(endpoint_ping)
        respuesta_ping=json.loads(solicitud_ping.get_data())
        msg=respuesta_ping["Mensaje"]
        self.assertEqual(solicitud_ping.status_code, 200)
        self.assertIn("Pong", msg)

    def test_env(self):
        endpoint_env='/env'
        solicitud_env=self.client.get(endpoint_env)
        self.assertEqual(solicitud_env.status_code, 200)

    def test_valida_crear_blmail(self):
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.tokenfijo)
        }

        endpoint_blacklist='/blacklists/'

        nuevo_blacklistmail={
            "email" : "caviedes72@yahoo.com",
            "app_uuid" : str(uuid.uuid4()),
            "blocked_reason" : "Por Mala Paga"
        }
        solicitud_nuevo_blmail=self.client.post(endpoint_blacklist, 
                                                data=json.dumps(nuevo_blacklistmail), 
                                                headers=headers)
        respuesta_nuevo_blmail=json.loads(solicitud_nuevo_blmail.get_data())
        self.assertEqual(solicitud_nuevo_blmail.status_code, 201)

        nuevo_blacklistmail={
            "app_uuid" : str(uuid.uuid4()),
            "blocked_reason" : "Por Mala Paga"
        }
        solicitud_nuevo_blmail=self.client.post(endpoint_blacklist, 
                                                data=json.dumps(nuevo_blacklistmail), 
                                                headers=headers)
        respuesta_nuevo_blmail=json.loads(solicitud_nuevo_blmail.get_data())
        msg=respuesta_nuevo_blmail["mensaje"]
        self.assertEqual(solicitud_nuevo_blmail.status_code, 400)
        self.assertEqual(msg, "Falta(n) uno o mas campos en la peticion.")

        nuevo_blacklistmail={
            "email" : "caviedes72@yahoo.com",
            "blocked_reason" : "Por Mala Paga"
        }
        solicitud_nuevo_blmail=self.client.post(endpoint_blacklist, 
                                                data=json.dumps(nuevo_blacklistmail), 
                                                headers=headers)
        respuesta_nuevo_blmail=json.loads(solicitud_nuevo_blmail.get_data())
        msg=respuesta_nuevo_blmail["mensaje"]
        self.assertEqual(solicitud_nuevo_blmail.status_code, 400)
        self.assertEqual(msg, "Falta(n) uno o mas campos en la peticion.")

        nuevo_blacklistmail={
            "email" : "caviedes72@yahoo.com",
            "app_uuid" : str(uuid.uuid4())
        }
        solicitud_nuevo_blmail=self.client.post(endpoint_blacklist, 
                                                data=json.dumps(nuevo_blacklistmail), 
                                                headers=headers)
        respuesta_nuevo_blmail=json.loads(solicitud_nuevo_blmail.get_data())
        msg=respuesta_nuevo_blmail["mensaje"]
        self.assertEqual(solicitud_nuevo_blmail.status_code, 400)
        self.assertEqual(msg, "Falta(n) uno o mas campos en la peticion.")

    def test_valida_consultar_blmail(self):
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.tokenfijo)
        }

        endpoint_blacklist='/blacklists/'

        nuevo_blacklistmail={
            "email" : "caviedes72@xyz.com",
            "app_uuid" : str(uuid.uuid4()),
            "blocked_reason" : "Por Mala Paga"
        }
        solicitud_nuevo_blmail=self.client.post(endpoint_blacklist, 
                                                data=json.dumps(nuevo_blacklistmail), 
                                                headers=headers)
        respuesta_nuevo_blmail=json.loads(solicitud_nuevo_blmail.get_data())
        self.assertEqual(solicitud_nuevo_blmail.status_code, 201)


        endpoint_blacklist='/blacklists/'+'caviedes72@xyz.com'
        solicitud_consulta_blmail=self.client.get(endpoint_blacklist, 
                                                headers=headers)
        respuesta_consulta_blmail=json.loads(solicitud_consulta_blmail.get_data())
        msg=respuesta_consulta_blmail["Encontrado"]
        self.assertEqual(solicitud_consulta_blmail.status_code, 200)
        self.assertTrue(msg)

        endpoint_blacklist='/blacklists/'+'caviedes72@abc.com'
        solicitud_consulta_blmail=self.client.get(endpoint_blacklist, 
                                                headers=headers)
        respuesta_consulta_blmail=json.loads(solicitud_consulta_blmail.get_data())
        msg=respuesta_consulta_blmail["Encontrado"]
        self.assertEqual(solicitud_consulta_blmail.status_code, 200)
        self.assertFalse(msg)

    def test_valida_token(self):
        headers={
        }

        endpoint_blacklist='/blacklists/'

        nuevo_blacklistmail={
            "email" : "caviedes72@xyz.com",
            "app_uuid" : str(uuid.uuid4()),
            "blocked_reason" : "Por Mala Paga"
        }
        solicitud_nuevo_blmail=self.client.post(endpoint_blacklist, 
                                                data=json.dumps(nuevo_blacklistmail), 
                                                headers=headers)
        respuesta_nuevo_blmail=json.loads(solicitud_nuevo_blmail.get_data())
        self.assertEqual("Missing JWT", respuesta_nuevo_blmail) 
        
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format("12345.6789.0")
        }

        solicitud_nuevo_blmail=self.client.post(endpoint_blacklist, 
                                                data=json.dumps(nuevo_blacklistmail), 
                                                headers=headers)
        respuesta_nuevo_blmail=json.loads(solicitud_nuevo_blmail.get_data())
        self.assertEqual("Usuario Desautorizado", respuesta_nuevo_blmail) 

        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NTc4NDI0MiwianRpIjoiYzBiMDBmMTMtNmRlYi00NTQ4LWE3ZDQtMDBhM2FlMGM5YzVlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjc1Nzg0MjQyLCJleHAiOjE2NzU3OTE0NDJ9.JmZI2kzjLdV69BBhzZBrrBTHFeAM8rnc7Ls1Lg_ohSQ")
        }

        solicitud_nuevo_blmail=self.client.post(endpoint_blacklist, 
                                                data=json.dumps(nuevo_blacklistmail), 
                                                headers=headers)
        respuesta_nuevo_blmail=json.loads(solicitud_nuevo_blmail.get_data())
        self.assertEqual("Signature verification failed", respuesta_nuevo_blmail) 

        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }

        solicitud_nuevo_blmail=self.client.post(endpoint_blacklist, 
                                                data=json.dumps(nuevo_blacklistmail), 
                                                headers=headers)
        respuesta_nuevo_blmail=json.loads(solicitud_nuevo_blmail.get_data())
        self.assertEqual("Ataque Detectado", respuesta_nuevo_blmail) 

