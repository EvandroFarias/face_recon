while True:
    detectar_róstos()
    if rosto_detectado:
        if processar_rosto:
            processar_rosto = False
            processar()