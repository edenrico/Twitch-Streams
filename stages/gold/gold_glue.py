import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

from pyspark.sql.functions import (
    col,
    to_date, 
    sum,      
    avg,      
    max,     
    count,   
    round as spark_round
)
from pyspark.sql.types import TimestampType

args = getResolvedOptions(sys.argv, ["JOB_NAME"]) 
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

dynamic_frame_silver = glueContext.create_dynamic_frame.from_catalog(
    database="db_silver",
    table_name="silver",
    transformation_ctx="silver_ctx"
)
print(f"Lendo {dynamic_frame_silver.count()} novos registros da camada Bronze.")

df_spark = dynamic_frame_silver.toDF()

df_silver_com_data = df_spark.withColumn(
    "data_agregacao", to_date(col("data_inicio_utc"))
)

print("Iniciando agregação para a camada Gold...")
df_fato_streams = df_silver_com_data.groupBy(
    "data_agregacao",
    "nome_streamer",
    "nome_categoria",
    "tipo_conteudo",
    "periodo_dia",
    "cod_idioma"
).agg(
    count("*").alias("total_de_streams"),
    spark_round(sum("duracao_min"), 2).alias("total_minutos_streamados"),
    spark_round(sum("horas_assistidas_total"), 2).alias("total_horas_assistidas"),
    spark_round(avg("viewers"), 2).alias("media_espectadores"),
    max("viewers").alias("pico_espectadores")
)

print("Agregação para a camada Gold concluída.")

dynamic_frame_gold_final = DynamicFrame.fromDF(
    df_fato_streams, glueContext, "dynamic_frame_gold_final"
)

glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame_gold_final,
    connection_type="s3",
    connection_options={
        "path": "s3://twitch-streams-s3/gold/",
    },
    format="parquet",
    transformation_ctx="dynamic_frame_gold_final"
)

job.commit()