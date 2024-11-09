import os
import vanna
from vanna.remote import VannaDefault
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

api_key = os.getenv("API_KEY")
db_host = os.getenv("DB_HOST")
db_password = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER")
db_name = os.getenv("DB_NAME")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

model_name = 'al-gaib'
index_name = "haderach"


pc = Pinecone(api_key=pinecone_api_key)

pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

vn = VannaDefault(model=model_name, api_key=api_key)

vn.connect_to_postgres(host=db_host,
                       dbname=db_name,
                       user=db_user,
                       password=db_password,
                       port=5432)


if __name__=="__main__":
    query = vn.run_sql(sql=''' SELECT 
    CONCAT(u."FirstName", ' ', u."LastName") AS FullName, 
    COUNT(q."Score") AS points,
    TO_CHAR(q."EndTime" - q."StartTime", 'HH24:MI:SS') AS duration
    FROM public."Users" AS u
    JOIN public."QuizSessions" AS q ON u."Id" = q."UserId"
    GROUP BY FullName, duration
    ORDER BY points DESC;
    ''')
    print("\n\n",query)

