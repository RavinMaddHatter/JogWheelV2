# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to use AWS SDK for Python (Boto3) to call Amazon Transcribe to make a
transcription of an audio file.

This script is intended to be used with the instructions for getting started in the
Amazon Transcribe Developer Guide here:
    https://docs.aws.amazon.com/transcribe/latest/dg/getting-started.html.
"""

import time
import boto3
import urllib.request
import json
import os
from botocore.exceptions import ClientError
import uuid


class translator:
    def __init__(self,s3Bucket="audioprocessing",profile="default"):
        self.s3Bucket=s3Bucket
        self.session = boto3.Session(profile_name=profile)
        self.transcribe_client = self.session.client('transcribe')
        self.s3_client = self.session.client('s3')
    def audioToText(self,fileName):
        obj_name=self.uploadFile(fileName)
        job_name=str(uuid.uuid4())
        url="s3://{}/{}".format(self.s3Bucket,obj_name)
        name="test.txt"
        path_to_transcript=self.transcribe(job_name, url)
        webURL=urllib.request.urlopen(path_to_transcript)
        file=json.loads(webURL.read().decode())
        with open(name, "w+") as text_file:
            text_file.write(file["results"]['transcripts'][0]['transcript'])
        self.deleteFile(obj_name)
    def uploadFile(self,fileName,object_name=None):
        if object_name is None:
            object_name = os.path.basename(fileName)
        try:
            response = self.s3_client.upload_file(fileName, self.s3Bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return "FAILED"
        return object_name
    def deleteFile(self, filename):
        try:
            self.s3_client.delete_object(Bucket=self.s3Bucket, Key=filename)
        except ClientError as e:
            logging.error(e)
            return False
        return True
    def transcribe(self,job_name, file_uri):
        self.transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': file_uri},
            MediaFormat='wav',
            LanguageCode='en-US'
        )

        max_tries = 360
        while max_tries > 0:
            max_tries -= 1
            job = self.transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            job_status = job['TranscriptionJob']['TranscriptionJobStatus']
            if job_status in ['COMPLETED', 'FAILED']:
                print(f"Job {job_name} is {job_status}.")
                
                if job_status == 'COMPLETED':
                    return job['TranscriptionJob']['Transcript']['TranscriptFileUri']
                break
            else:
                print(f"Waiting for {job_name}. Current status is {job_status}.")
            time.sleep(10)



if __name__ == '__main__':
    trans=translator()
    trans.audioToText("Test Files\\testAudio.wav")
