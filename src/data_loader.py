import pandas as pd
import os
import io

def load_university_data():
    """
    Load university data from CSV or create it from the provided string
    Returns a pandas DataFrame with university information
    """
    csv_path = os.path.join('data', 'universities.csv')
    
    # Check if the CSV file exists
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    
    # If not, create the CSV from our data string
    csv_data = """University,Type,Funding,ResearchOutput,Latitude,Longitude,City,ShortName
University of the Philippines,Public,544,650,14.654936,121.064941,Quezon City,UP
De La Salle University,Private,320,400,14.563650,120.994060,Manila,DLSU
Ateneo de Manila University,Private,290,380,14.640373,121.077638,Quezon City,ADMU
University of Santo Tomas,Private,225,310,14.610484,120.989690,Manila,UST
Mapua University,Private,175,220,14.590100,120.987160,Manila,Mapua
Polytechnic University of the Philippines,Public,120,180,14.599440,120.991030,Manila,PUP
Far Eastern University,Private,110,140,14.601500,120.992400,Manila,FEU
Philippine Normal University,Public,85,110,14.587620,120.980580,Manila,PNU
Adamson University,Private,80,105,14.598250,120.987260,Manila,Adamson
Technological University of the Philippines,Public,78,95,14.592680,120.983850,Manila,TUP
University of the East,Private,65,90,14.601790,120.987880,Manila,UE
Philippine Science High School,Public,67,85,14.647500,121.055600,Quezon City,PSHS
National University,Private,55,75,14.605900,120.992080,Manila,NU
Pamantasan ng Lungsod ng Maynila,Public,52,75,14.587500,120.979810,Manila,PLM
Asia Pacific College,Private,40,50,14.548490,121.019730,Makati,APC
Miriam College,Private,35,45,14.639050,121.074900,Quezon City,Miriam"""
    
    # Create a DataFrame from the string
    df = pd.read_csv(io.StringIO(csv_data))
    
    # Save to CSV for future use
    os.makedirs('data', exist_ok=True)
    df.to_csv(csv_path, index=False)
    
    return df

def get_university_stats():
    """
    Calculate and return statistics about universities
    """
    df = load_university_data()
    
    stats = {
        'total_universities': len(df),
        'public_count': len(df[df['Type'] == 'Public']),
        'private_count': len(df[df['Type'] == 'Private']),
        'total_funding': df['Funding'].sum(),
        'total_research_output': df['ResearchOutput'].sum(),
        'avg_funding_public': df[df['Type'] == 'Public']['Funding'].mean(),
        'avg_funding_private': df[df['Type'] == 'Private']['Funding'].mean(),
        'top_funded': df.sort_values('Funding', ascending=False).iloc[0]['University'],
        'cities': df['City'].value_counts().to_dict()
    }
    
    return stats
