# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with Amazon Rekognition to
recognize people, objects, and text in images.

The usage demo in this file uses images in the .media folder. If you run this code
without cloning the GitHub repository, you must first download the image files from
    https://github.com/awsdocs/aws-doc-sdk-examples/tree/master/python/example_code/rekognition/.media
"""

import json
import logging
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
#from flask import request as requests
import requests
from flaskr.api.managers.rekognition_objects import RekognitionFace, RekognitionCelebrity, RekognitionLabel, RekognitionModerationLabel, RekognitionText, show_bounding_boxes, show_polygons

logger = logging.getLogger(__name__)


class RekognitionImage:
    """
    Encapsulates an Amazon Rekognition image. This class is a thin wrapper
    around parts of the Boto3 Amazon Rekognition API.
    """

    def __init__(self, image, image_name, rekognition_client):
        """
        Initializes the image object.

        :param image: Data that defines the image, either the image bytes or
                      an Amazon S3 bucket and object key.
        :param image_name: The name of the image.
        :param rekognition_client: A Boto3 Rekognition client.
        """
        self.image = image
        self.image_name = image_name
        self.rekognition_client = rekognition_client

    @classmethod
    def from_file(cls, image_file_name, rekognition_client, image_name=None):
        """
        Creates a RekognitionImage object from a local file.

        :param image_file_name: The file name of the image. The file is opened and its
                                bytes are read.
        :param rekognition_client: A Boto3 Rekognition client.
        :param image_name: The name of the image. If this is not specified, the
                           file name is used as the image name.
        :return: The RekognitionImage object, initialized with image bytes from the
                 file.
        """
        with open(image_file_name, 'rb') as img_file:
            image = {'Bytes': img_file.read()}
        name = image_file_name if image_name is None else image_name
        return cls(image, name, rekognition_client)

    @classmethod
    def from_bucket(cls, s3_object, rekognition_client):
        """
        Creates a RekognitionImage object from an Amazon S3 object.

        :param s3_object: An Amazon S3 object that identifies the image. The image
                          is not retrieved until needed for a later call.
        :param rekognition_client: A Boto3 Rekognition client.
        :return: The RekognitionImage object, initialized with Amazon S3 object data.
        """
        image = {
            'S3Object': {
                'Bucket': s3_object.bucket_name,
                'Name': s3_object.key
            }
        }
        return cls(image, s3_object.key, rekognition_client)

    def detect_faces(self):
        """
        Detects faces in the image.

        :return: The list of faces found in the image.
        """
        try:
            response = self.rekognition_client.detect_faces(Image=self.image, Attributes=['ALL'])
            faces = [RekognitionFace(face) for face in response['FaceDetails']]
            logger.info("Detected %s faces.", len(faces))
        except ClientError:
            logger.exception("Couldn't detect faces in %s.", self.image_name)
            raise
        else:
            return faces

    def compare_faces(self, target_image, similarity):
        """
        Compares faces in the image with the largest face in the target image.

        :param target_image: The target image to compare against.
        :param similarity: Faces in the image must have a similarity value greater
                           than this value to be included in the results.
        :return: A tuple. The first element is the list of faces that match the
                 reference image. The second element is the list of faces that have
                 a similarity value below the specified threshold.
        """
        try:
            response = self.rekognition_client.compare_faces(
                SourceImage=self.image,
                TargetImage=target_image.image,
                SimilarityThreshold=similarity)
            matches = [
                RekognitionFace(match['Face'])
                for match in response['FaceMatches']
            ]
            unmatches = [
                RekognitionFace(face) for face in response['UnmatchedFaces']
            ]
            logger.info("Found %s matched faces and %s unmatched faces.",
                        len(matches), len(unmatches))
        except ClientError:
            logger.exception("Couldn't match faces from %s to %s.",
                             self.image_name, target_image.image_name)
            raise
        else:
            return matches, unmatches

    def detect_labels(self, max_labels):
        """
        Detects labels in the image. Labels are objects and people.

        :param max_labels: The maximum number of labels to return.
        :return: The list of labels detected in the image.
        """
        try:
            response = self.rekognition_client.detect_labels(
                Image=self.image, MaxLabels=max_labels)
            labels = [RekognitionLabel(label) for label in response['Labels']]
            logger.info("Found %s labels in %s.", len(labels), self.image_name)
        except ClientError:
            logger.info("Couldn't detect labels in %s.", self.image_name)
            raise
        else:
            return labels

    def detect_moderation_labels(self):
        """
        Detects moderation labels in the image. Moderation labels identify content
        that may be inappropriate for some audiences.

        :return: The list of moderation labels found in the image.
        """
        try:
            response = self.rekognition_client.detect_moderation_labels(
                Image=self.image)
            labels = [
                RekognitionModerationLabel(label)
                for label in response['ModerationLabels']
            ]
            logger.info("Found %s moderation labels in %s.", len(labels),
                        self.image_name)
        except ClientError:
            logger.exception("Couldn't detect moderation labels in %s.",
                             self.image_name)
            raise
        else:
            return labels

    def detect_text(self):
        """
        Detects text in the image.

        :return The list of text elements found in the image.
        """
        try:
            response = self.rekognition_client.detect_text(Image=self.image)
            texts = [
                RekognitionText(text) for text in response['TextDetections']
            ]
            logger.info("Found %s texts in %s.", len(texts), self.image_name)
        except ClientError:
            logger.exception("Couldn't detect text in %s.", self.image_name)
            raise
        else:
            return texts

    def recognize_celebrities(self):
        """
        Detects celebrities in the image.

        :return: A tuple. The first element is the list of celebrities found in
                 the image. The second element is the list of faces that were
                 detected but did not match any known celebrities.
        """
        try:
            response = self.rekognition_client.recognize_celebrities(
                Image=self.image)
            celebrities = [
                RekognitionCelebrity(celeb)
                for celeb in response['CelebrityFaces']
            ]
            other_faces = [
                RekognitionFace(face) for face in response['UnrecognizedFaces']
            ]
            logger.info("Found %s celebrities and %s other faces in %s.",
                        len(celebrities), len(other_faces), self.image_name)
        except ClientError:
            logger.exception("Couldn't detect celebrities in %s.",
                             self.image_name)
            raise
        else:
            return celebrities, other_faces


def face_from_url(url, shoulDisplayImageBoundingBox):
    print('-' * 88)
    print("Face Rekognition Demo ")
    print('-' * 88)

    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')
    rekognition_client = boto3.client('rekognition')

    image_response = requests.get(url)
    print(image_response.content)
    image = RekognitionImage({'Bytes': image_response.content}, "image",
                             rekognition_client)

    print(f"Detecting faces in {image.image_name}...")
    faces = image.detect_faces()
    faces_list = []

    print(f"Found {len(faces)} faces, here are the first three.")
    for face in faces[:3]:
        faces_list.append(face.to_dict())

    if shoulDisplayImageBoundingBox :
        show_bounding_boxes(
            image.image['Bytes'], [
                [face.bounding_box for face in faces]],
            ['aqua'])
    
    print("Thanks for watching!")
    print('-'*88)
    
    return faces_list


def face_from_local_file(url, shoulDisplayImageBoundingBox=False, args=None):

    faces_list = []

    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')
    rekognition_client = boto3.client('rekognition')

    file_name = "flaskr/images/" + url

    image = RekognitionImage.from_file(file_name, rekognition_client)

    faces = image.detect_faces()             
        
    # Display the image and bounding boxes of each face.
    if shoulDisplayImageBoundingBox:
        show_bounding_boxes(image.image['Bytes'],
                            [[face.bounding_box for face in faces]], ['aqua'])

    # If arg is not None, then it is a list of arguments
    # split the arg into list
    if args is not None:
        selectedAttributes = []

        #arg_list = args.split(',')

        for face in faces[:3]:
            faces_list.append(face.to_dict_args())


        #return json.dumps(faces_list)

        # for each args
        #for arg in arg_list:
        for face in faces_list:
            # get the interested attribute with the argument
            selectedAttributes.append(face[args])

        return json.dumps(selectedAttributes)

    else:

        for face in faces[:3]:
            faces_list.append(face.to_dict())
        return faces_list

# This is a test
def celebrity_demo():

    print('-' * 88)
    print("Welcome to the Amazon Rekognition celibrity detection demo!")
    print('-' * 88)

    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')
    rekognition_client = boto3.client('rekognition')
    celebrity_file_name = "flaskr/images/pexels-pixabay-53370.jpg"
    celebrity_image = RekognitionImage.from_file(celebrity_file_name,
                                                 rekognition_client)

    print(f"Detecting celebrities in {celebrity_image.image_name}...")
    celebs, others = celebrity_image.recognize_celebrities()
    print(f"Found {len(celebs)} celebrities.")
    for celeb in celebs:
        pprint(celeb.to_dict())
    show_bounding_boxes(celebrity_image.image['Bytes'],
                        [[celeb.face.bounding_box for celeb in celebs]],
                        ['aqua'])
    input("Press Enter to continue.")