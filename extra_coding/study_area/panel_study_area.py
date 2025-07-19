from PIL import Image

def create_panel():
    # Carregar imagens
    image_large = Image.open("/home/bianca/Documentos/masters/experiments/study_area/big_study_area.png")
    image_small1 = Image.open("/home/bianca/Documentos/masters/experiments/study_area/Yucatan.png")
    image_small2 = Image.open("/home/bianca/Documentos/masters/experiments/study_area/Houston.png")
    
    # Definir dimensões para o painel final
    panel_width = image_large.width + image_small2.width + 250
    panel_height = max(image_large.height, image_small1.height + image_small2.height)
    
    # Criar painel em branco
    panel = Image.new("RGB", (panel_width, panel_height), (255, 255, 255))
    
    # Colar imagem grande centralizada verticalmente
    y_large = (panel.height - image_large.height) // 2
    panel.paste(image_large, (0, y_large))

    # Coordenada x para small2 (imagem pequena 2)
    x_small2 = image_large.width + 90
    y_small2 = (panel.height - image_small2.height)  # Centraliza small2 verticalmente
    panel.paste(image_small2, (x_small2, y_small2))

    # Coordenada x para small1 (alinhando centro com small2)
    x_small1 = x_small2 + (image_small2.width // 2) - (image_small1.width // 2)
    y_small1 = y_small2 - image_small1.height - 10  # Posiciona acima de small2 com 10px de margem
    panel.paste(image_small1, (x_small1, y_small1))
    
    # Salvar painel final
    panel.save("panel_image.png")
    # panel.show()

create_panel()