import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

from pyspark.sql.functions import (
    col, when, lit, round as spark_round, floor
)
from pyspark.sql.types import TimestampType

args = getResolvedOptions(sys.argv, ["JOB_NAME"]) 
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

dynamic_frame_bronze = glueContext.create_dynamic_frame.from_catalog(
    database="db_raw",
    table_name="raw",
    transformation_ctx="bronze_ctx"
)
print(f"Lendo {dynamic_frame_bronze.count()} novos registros da camada Bronze.")

df_spark = dynamic_frame_bronze.toDF()

# 3.2. Tratar valores nulos (AGORA VAI FUNCIONAR)
# Usando o .fillna() do Spark no DataFrame Spark
df_spark = df_spark.fillna(
    {"categoria": "Desconhecido", "game_id": "DESCONHECIDO"}
)

# 3.3. Renomear campos (usando .withColumnRenamed() do Spark)
df_spark = df_spark.withColumnRenamed("streamer", "nome_streamer") \
                   .withColumnRenamed("categoria", "nome_categoria") \
                   .withColumnRenamed("idioma", "cod_idioma") \
                   .withColumnRenamed("inicio", "data_inicio_utc") \
                   .withColumnRenamed("dia_semana", "nome_dia_semana") \
                   .withColumnRenamed("hora", "hora_inicio_utc")

# 3.4. Engenharia de Features (Baseada na nossa conversa - JÁ ESTAVA CORRETO)

# A. Criar 'tipo_conteudo' ("Game" vs "Não-Game")
categorias_nao_game = [
    'Just Chatting', 'Sports', 'Virtual Casino', 'IRL',
    'Software and Game Development', 'Always On', 'Desconhecido',
    'Slots', 'Music', 'ASMR', 'Talk Shows & Podcasts'
]
df_spark = df_spark.withColumn(
    "tipo_conteudo",
    when(col("nome_categoria").isin(categorias_nao_game), "Não-Game")
    .otherwise("Game")
)

# B. Criar 'periodo_dia' (baseado na 'hora_inicio_utc')
df_spark = df_spark.withColumn(
    "periodo_dia",
    when((col("hora_inicio_utc") >= 0) & (col("hora_inicio_utc") <= 5), "Madrugada")
    .when((col("hora_inicio_utc") >= 6) & (col("hora_inicio_utc") <= 11), "Manhã")
    .when((col("hora_inicio_utc") >= 12) & (col("hora_inicio_utc") <= 17), "Tarde")
    .otherwise("Noite")
)

# C. Criar 'horas_assistidas_total' (Métrica de volume)
df_spark = df_spark.withColumn(
    "horas_assistidas_total",
    spark_round(col("viewers") * (col("duracao_min") / 60), 2)
)

# D. Converter string 'data_inicio_utc' para timestamp (crucial para Data Science)
df_spark = df_spark.withColumn(
    "data_inicio_utc",
    col("data_inicio_utc").cast(TimestampType())
)

# 3.5. Converter de volta para DynamicFrame (no final de tudo)
dynamic_frame_silver_final = DynamicFrame.fromDF(
    df_spark, glueContext, "dynamic_frame_silver_final"
)

# --- 4. CARREGAR (Load) ---
# (Esta parte já estava correta)
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame_silver_final,
    connection_type="s3",
    connection_options={
        "path": "s3://twitch-streams-s3/silver/",
        #"partitionKeys": ["year", "month", "day"] # Mantém o particionamento
    },
    format="parquet",
    transformation_ctx="dynamic_frame_silver_write"
)

job.commit()