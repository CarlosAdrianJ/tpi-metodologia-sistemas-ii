from src.consola import ConsolaSolicitudes
from src.repositorio import RepositorioSolicitudesJSON
from src.servicio import ServicioSolicitudes


def main() -> None:
    repositorio = RepositorioSolicitudesJSON()
    servicio = ServicioSolicitudes(repositorio)
    consola = ConsolaSolicitudes(servicio)
    consola.ejecutar()


if __name__ == "__main__":
    main()