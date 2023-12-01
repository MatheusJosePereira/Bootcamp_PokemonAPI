from flask import Flask, render_template, request
from models.pokemonlab import Pokemon
import requests





app = Flask(__name__)




@app.route("/")
def index():
    return render_template('index.html')

@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    # Obtém o nome do Pokémon do formulário e transforma em minúsculas (por conta da API)
    nome_pokemon = request.form["nome"].lower()
    pokemon = Pokemon(nome_pokemon, "",[])  # Cria uma instância da classe Pokemon

    try:
        # Faz uma requisição à API  para obter informações do Pokémon
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nome_pokemon}")

        # Lança uma exceção para códigos de status diferentes
        res.raise_for_status()

        # Converte a resposta JSON em um dicionário
        data = res.json()

        tipos = [tipo["type"]["name"] for tipo in data["types"]]
        pokemon.tipos = tipos

        # Obtém a URL da imagem frontal do Pokémon a partir dos dados da API
        result = data["sprites"]["front_default"]
        pokemon.foto = result
    except requests.exceptions.HTTPError:
        # Trata erros HTTP 404 que aparece no terminal
        if res.status_code == 404:
            return "Pokemon não encontrado volte a página e tente novamente!"
        else:
            return "Erro HTTP: "
    except Exception as e:
        # Trata outros erros
        return f"Erro: {e}"

    
    return render_template("index.html",
                           nome=pokemon.nome,
                           foto=pokemon.foto,
                           tipos=pokemon.tipos
                           )

if __name__ == '__main__':
    app.run(debug=True)