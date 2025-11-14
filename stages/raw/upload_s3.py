import boto3
from botocore.exceptions import NoCredentialsError
import os
from datetime import datetime, timezone
import io
import pandas as pd

def s3_upload_parquet(df, prefix="raw"):
    now = datetime.now(timezone.utc)
    bucket = os.getenv("S3_BUCKET_NAME")
    #file_name = f"twitch_streams_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    file_name = f"twitch_streams_{now.strftime('%Y%m%d_%H%M%S')}.parquet"
    object_name = f"{prefix}/{file_name}"

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )

    try:
        #json_buffer = df.to_json(orient="records", force_ascii=False, indent=2)
        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False, engine="pyarrow", compression="snappy")
        buffer.seek(0)
        
        s3_client.put_object(
            Body=buffer.getvalue(),
            Bucket=bucket,
            Key=object_name,
            ContentType="application/parquet-streams"
        )
        print(f"Arquivo {object_name} enviado para o bucket {bucket}.")
    except NoCredentialsError:
        print("Credenciais AWS não encontradas.")
    except Exception as e:
        print(f"Erro ao enviar para o S3: {e}")
