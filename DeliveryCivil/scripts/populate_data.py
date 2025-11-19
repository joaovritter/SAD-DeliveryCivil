"""
Script para popular o sistema com datasets de exemplo
Copia os arquivos de exemplo para o diretório de dados processados
"""
import shutil
from pathlib import Path
from datetime import datetime

def populate_data():
    """Copia arquivos de exemplo para data/raw"""
    print("=" * 60)
    print("📊 POPULANDO SISTEMA COM DATASETS DE EXEMPLO")
    print("=" * 60)
    
    # Diretórios
    examples_dir = Path("data/examples")
    raw_dir = Path("data/raw")
    
    # Criar diretório se não existir
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Arquivos a copiar
    files_to_copy = [
        ("vendas_exemplo.csv", "vendas"),
        ("estoque_exemplo.csv", "estoque"),
        ("compras_exemplo.csv", "compras")
    ]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    copied = []
    for source_file, prefix in files_to_copy:
        source_path = examples_dir / source_file
        
        if not source_path.exists():
            print(f"❌ Arquivo não encontrado: {source_path}")
            continue
        
        # Nome do arquivo de destino
        dest_file = f"{prefix}_{timestamp}.csv"
        dest_path = raw_dir / dest_file
        
        # Copiar arquivo
        try:
            shutil.copy2(source_path, dest_path)
            print(f"✅ Copiado: {source_file} → {dest_file}")
            copied.append(dest_file)
        except Exception as e:
            print(f"❌ Erro ao copiar {source_file}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("📊 RESUMO")
    print("=" * 60)
    print(f"✅ Arquivos copiados: {len(copied)}/{len(files_to_copy)}")
    
    if copied:
        print("\n📁 Arquivos em data/raw/:")
        for file in copied:
            print(f"   - {file}")
        
        print("\n🎉 Sistema populado com sucesso!")
        print("   Agora você pode acessar /reports para ver as análises")
    else:
        print("\n⚠️  Nenhum arquivo foi copiado")

if __name__ == "__main__":
    populate_data()

