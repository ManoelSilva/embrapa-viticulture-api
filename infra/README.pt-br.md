[English version](README.md)

# Infraestrutura como Código (IaC) para API de Viticultura da Embrapa

Este diretório contém a configuração do Terraform e scripts de implantação para a API de Viticultura da Embrapa na AWS.

## Pré-requisitos

- Conta AWS com permissões apropriadas
- AWS CLI configurado com credenciais
- Terraform instalado localmente
- Repositório GitHub com GitHub Actions habilitado
- Par de chaves SSH para acesso à instância EC2 (chave privada nos segredos do GitHub, chave pública no EC2)

## Instruções de Configuração

1. Configure as credenciais AWS:
   ```bash
   aws configure
   ```

2. Inicialize o Terraform:
   ```bash
   cd infra
   terraform init
   ```

3. Planeje a infraestrutura:
   ```bash
   terraform plan
   ```

4. Aplique a infraestrutura:
   ```bash
   terraform apply
   ```

## Configuração do GitHub Actions

1. Adicione os seguintes segredos ao seu repositório GitHub:
   - `AWS_ACCESS_KEY_ID`: Sua chave de acesso AWS
   - `AWS_SECRET_ACCESS_KEY`: Sua chave secreta AWS
   - `SSH_PRIVATE_KEY`: Sua chave privada SSH para acesso à instância EC2
   - `EC2_INSTANCE_ID`: O ID da instância EC2
   - `EC2_SECURITY_GROUP_ID`: O ID do grupo de segurança da instância EC2
   - `MOTHERDUCK_TOKEN`: Token para acessar o motherduck

2. O workflow do GitHub Actions irá automaticamente:
   - Executar testes Python usando pytest
   - Implantar alterações quando mescladas na branch feature/cloud_deploy
   - Permitir dinamicamente SSH do IP do runner durante a implantação e removê-lo após
   - Conectar via SSH à instância EC2 e executar `deploy.sh`, que puxa o código mais recente e reinicia o serviço

## Processo de Implantação

A implantação agora é realizada puxando o código mais recente do GitHub diretamente na instância EC2. Não há mais empacotamento ou cópia de arquivos do runner:

1. **Provisionamento de infraestrutura** (EC2, VPC, etc.)
2. **Implantação da aplicação:**
   - Atualizações do sistema e instalação de pacotes
   - Configuração do ambiente virtual Python
   - **O código da aplicação é puxado do GitHub** (usando `git pull` ou `git clone`)
   - Configuração do serviço systemd
   - Reinício do serviço da aplicação

### Script de Implantação Local

Você também pode implantar manualmente usando o script PowerShell fornecido:

```powershell
./deploy_locally.ps1 <EC2_PUBLIC_IP> <MOTHERDUCK_TOKEN>
```
- Este script irá conectar via SSH à instância EC2, puxar o código mais recente do GitHub, instalar dependências e reiniciar o serviço.
- Certifique-se de que sua chave privada SSH esteja disponível em `~/.ssh/id_rsa` e seu repositório esteja definido no script (padrão: `manoelsilva/embrapa-viticulture-api`).

## Componentes da Infraestrutura

- VPC com sub-rede pública
- Gateway de Internet
- Tabela de Rotas
- Grupo de Segurança (permitindo SSH e HTTP)
- Instância EC2 (t2.micro - Elegível para Free Tier)
  - Ubuntu 22.04 LTS
  - Volume EBS de 8GB (Elegível para Free Tier)

## Notas de Segurança

- O grupo de segurança permite HTTP (porta 80) de qualquer lugar por padrão, e SSH (porta 22) apenas para o var ssh_access_cidr configurado em [variables.tf](variables.tf), mas **o workflow do GitHub Actions restringe dinamicamente o acesso SSH ao IP do runner durante a implantação e o remove após**.
- Considere restringir o acesso SSH a intervalos de IP específicos em produção.
- Use o AWS Systems Manager Session Manager para acesso seguro em vez de SSH quando possível.
- A aplicação é executada sob um serviço systemd dedicado.
- O diretório da aplicação pertence ao usuário ubuntu.

## Notas do Pipeline CI/CD

- Testes Python (pytest) são executados antes de qualquer implantação.
- A implantação só prossegue se os testes passarem.
- O código implantado é sempre o commit exato que acionou o workflow.

## Considerações de Custo

Esta infraestrutura usa recursos elegíveis para o AWS Free Tier:
- Instância t2.micro
- Volume EBS de 8GB
- Componentes básicos de rede

Monitore seu uso da AWS para permanecer dentro dos limites do Free Tier.

## Monitoramento

Para verificar o status da aplicação:
```bash
sudo systemctl status embrapa-viticulture
```

Para visualizar os logs da aplicação:
```bash
sudo journalctl -u embrapa-viticulture -f
``` 