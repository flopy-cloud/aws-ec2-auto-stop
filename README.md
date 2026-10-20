# # Apagado y encendido automático de EC2 con Terraform

## Objetivo
Evitar gastar crédito en instancias EC2 que no se usan de noche. Una función Lambda apaga las instancias a las 22:00 y las vuelve a prender a las 08:00 (hora de Argentina), de forma automática.

## Arquitectura
- **EventBridge:** dos reglas con horario (cron), una para apagar y otra para prender.
- **Lambda (Python 3.13):** busca las instancias con la etiqueta `AutoStop=true` y las apaga o las prende, según el parámetro que recibe.
- **IAM:** rol con permisos mínimos. Solo puede listar instancias y apagar o prender las que tengan la etiqueta `AutoStop=true`.
- **EC2 de prueba:** una `t3.micro` con la etiqueta `AutoStop=true`.

Toda la infraestructura está definida con **Terraform** en la región `us-east-1`.

## Cómo funciona
1. A las 01:00 UTC (22:00 en Argentina), EventBridge invoca la Lambda con `{"action": "stop"}`.
2. A las 11:00 UTC (08:00 en Argentina), la invoca con `{"action": "start"}`.
3. La Lambda consulta las instancias con la etiqueta `AutoStop=true` en el estado correspondiente y les aplica la acción.

## Cómo usarlo
```bash
terraform init
terraform plan
terraform apply
```

Para probarlo sin esperar al horario, invoqué la Lambda manualmente:
```bash
aws lambda invoke --function-name ec2-auto-stop \
  --cli-binary-format raw-in-base64-out \
  --payload '{"action":"stop"}' salida.json
```

Para eliminar todo:
```bash
terraform destroy
```

## Resultados

### Instancia apagada por la Lambda
<img width="1028" height="70" alt="Captura de pantalla de 2026-10-19 20-31-20" src="https://github.com/user-attachments/assets/55cc330f-6c61-4ced-9f8b-b73475ebd5dd" />


### Instancia prendida por la Lambda
<img width="1363" height="76" alt="Captura de pantalla de 2026-10-19 20-33-33" src="https://github.com/user-attachments/assets/1d9dd9cc-5c0e-4774-84cc-a0744a467629" />



### Reglas de EventBridge
<img width="1280" height="186" alt="photo_5094027433391885718_y" src="https://github.com/user-attachments/assets/5d9d369b-6e08-4d69-ae5c-deaeccfdd46a" />



### Despliegue con Terraform
<img width="507" height="56" alt="Captura de pantalla de 2026-10-19 21-00-41" src="https://github.com/user-attachments/assets/2f175149-6dbf-4d6e-8b5c-0ae4bcf97ac4" />


## Qué aprendí
- EventBridge trabaja en hora UTC, así que hay que convertir el horario local al definir los cron.
- Con etiquetas y una condición en la política de IAM, la Lambda solo puede tocar las instancias que yo marco.
- Con Terraform puedo crear y destruir toda la infraestructura con un comando, y así controlo el costo.

## Costo
Prácticamente cero. Lambda y EventBridge entran en el free tier, y la instancia de prueba la destruí después de las pruebas.<img width="1363" height="76" alt="Captura de pantalla de 2026-10-19 20-33-33" src="https://github.com/user-attachments/assets/deeb32e0-3688-42b7-a4a0-de0b7b8abe8c" />
aws-ec2-auto-stop
