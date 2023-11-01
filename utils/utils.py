import os
import pymongo


def lerArquivo(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prev_dir = os.path.dirname(script_dir)
    file_path = os.path.join(prev_dir, filename)

    return open(file_path).read().strip().replace(' ', '%20').split('\n')


def conectar_mongodb():
    MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    client = pymongo.MongoClient(MONGODB_URI)
    db = client["autohub"]
    collection = db["veiculos"]
    return collection


def inserir_dados_mongodb(collection, veiculoNome, veiculoUrl, preco, local, veiculoImg, origem):
    data_to_insert = {
        "veiculo": veiculoNome,
        "url": veiculoUrl,
        "price": preco,
        "local": local,
        "veiculoImg": veiculoImg,
        "origem": origem
    }
    collection.insert_one(data_to_insert)
