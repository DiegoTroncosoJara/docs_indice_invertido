from urllib.parse import urlparse


def obtener_dominio_raiz(url):
    parsed_url = urlparse(url)
    dominio_raiz = parsed_url.scheme + '://www.' + parsed_url.netloc
    return dominio_raiz


# /api/elasticsearch/refresh

#entrega el nombre del dominio 
def obtainDomainPath(path):
    """
    Obtiene el dominio de un path
    """
    # print("path = ",path)

    parsed_url = urlparse(path)
    domain_name = parsed_url.netloc
    
    if domain_name.startswith("www."):
        domain_name = domain_name[4:]

    if "." in domain_name:
        domain_name = domain_name[:domain_name.index(".")]
    #print(domain_name)
    return domain_name
    
