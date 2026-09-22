from fastapi import APIRouter, Request, Depends

from dependencies.http import get_http_client

from services.evolution.instances import find_instances, create_instance, connect_instance


router = APIRouter(
    prefix='/instances',
    tags = ['Instances']
)


@router.get('/qrcode/')
async def get_qrcode(
    client = Depends(get_http_client)
): 
    

    response = await find_instances(client=client)
    instances_list = response.json()

    #Se não houver sessões, deverá ser criado uma
    if not len(instances_list):
        await create_instance(name="fake-analyser", client=client)

        #Alterar a lista de instâncias com a instância nova
        response = await find_instances(client=client)
        instances_list = response.json()

    # Captura o nome da primeira instância que encontrar
    instance_name = instances_list[0]["name"]


    # Realiza a conexão da instância
    response = await connect_instance(name=instance_name, client=client)

    return response.json()

    