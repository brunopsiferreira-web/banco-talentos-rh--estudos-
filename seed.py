import random
import os
from faker import Faker
from fpdf import FPDF
from app.database import SessionLocal

# Importamos os MÓDULOS (arquivos)
import app.models.job as job_module
import app.models.candidate as candidate_module

fake = Faker('pt_BR')

def create_fake_pdf(file_path):
    """Cria um arquivo PDF real para que o botão 'Ver CV' funcione no navegador"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Curriculo Gerado Automaticamente (Teste)", ln=1, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, txt=f"Este e um documento de teste gerado para simular o currículo de um candidato no sistema de RH.\n\nData de geracao: {fake.date()}")
        
        # Garante que a pasta 'uploads' existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        pdf.output(file_path)
    except Exception as e:
        print(f"Erro ao criar PDF: {e}")

def get_class_from_module(module):
    """Varre o arquivo para encontrar a classe que herda do SQLAlchemy"""
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and hasattr(obj, '__tablename__'):
            return obj
    return None

def seed_database():
    db = SessionLocal()
    
    # 1. Detecta as classes automaticamente
    JobClass = get_class_from_module(job_module)
    CandidateClass = get_class_from_module(candidate_module)

    if not JobClass or not CandidateClass:
        print("❌ Erro: Não foi possível localizar as classes Job ou Candidate nos modelos.")
        return

    print(f"🌱 Iniciando população do banco...")
    print(f"Detectado: Vagas ({JobClass.__name__}) | Candidatos ({CandidateClass.__name__})")

    # 2. Criar Vagas Fictícias
    vagas_list = [
        "Desenvolvedor Python Full Stack", 
        "Analista de Recrutamento Tech", 
        "UX Designer Senior", 
        "Gerente de Projetos TI", 
        "Engenheiro de Dados",
        "Especialista DevOps"
    ]
    
    for titulo in vagas_list:
        vaga = JobClass(
            title=titulo,
            description=fake.paragraph(nb_sentences=4),
            status=random.choice(["aberta", "em análise", "fechada"])
        )
        db.add(vaga)
    
    # 3. Criar Candidatos e seus respectivos PDFs
    print(f"📄 Gerando 15 candidatos e currículos...")
    formacoes = ["Ciência da Computação", "Psicologia", "Gestão de RH", "Design Gráfico", "Engenharia de Software"]

    for _ in range(15):
        p_nome = fake.first_name()
        u_nome = fake.last_name()
        
        # Define caminho do arquivo único
        nome_arquivo = f"cv_{p_nome.lower()}_{random.randint(1000, 9999)}.pdf"
        caminho_relativo = f"uploads/{nome_arquivo}"
        caminho_absoluto = os.path.join(os.getcwd(), caminho_relativo)

        # Cria o PDF físico
        create_fake_pdf(caminho_absoluto)

        # Cria o registro no banco
        candidato = CandidateClass(
            first_name=p_nome,
            last_name=u_nome,
            email=fake.email(),
            phone=fake.cellphone_number(),
            education=random.choice(formacoes),
            career_objective=f"Meu objetivo é atuar como {random.choice(vagas_list)}.",
            resume_path=caminho_relativo  # Caminho que o sistema usa para abrir
        )
        db.add(candidato)
    
    try:
        db.commit()
        print("✅ Sucesso: Dados e arquivos gerados com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao salvar no banco: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Certifique-se de ter instalado: pip install fpdf faker
    seed_database()