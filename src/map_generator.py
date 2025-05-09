import folium
from folium.plugins import HeatMap, MarkerCluster
from src.data_loader import load_university_data

def generate_research_map():
    """
    Generate an interactive map showing research funding for Metro Manila universities
    Returns HTML string of the map
    """
    # Load university data
    df = load_university_data()
    
    # Normalize funding for marker size
    max_funding = df['Funding'].max()
    min_funding = df['Funding'].min()
    df['MarkerSize'] = ((df['Funding'] - min_funding) / (max_funding - min_funding) * 25) + 10
    
    # Create the map centered on Metro Manila
    metro_manila_map = folium.Map(
        location=[14.58, 121.00], 
        zoom_start=12,
        tiles="cartodbpositron"
    )
    
    # Add alternative tile layers
    folium.TileLayer('openstreetmap', name='OpenStreetMap').add_to(metro_manila_map)
    folium.TileLayer('Stamen Toner', name='Stamen Toner').add_to(metro_manila_map)
    folium.TileLayer('Stamen Terrain', name='Stamen Terrain').add_to(metro_manila_map)
    
    # Add title
    title_html = '''
        <div style="position: fixed; 
            top: 10px; left: 50px; width: 600px; height: 90px; 
            background-color:white; border-radius: 5px; border: 2px solid grey;
            z-index: 9999; font-family: Arial; padding: 10px">
            <h2 style="margin: 0; text-align: center">Federal Funding for Research and Development in Metro Manila (2024)</h2>
            <h4 style="margin: 5px 0 0 0; text-align: center">
                Each circle represents a university: 
                <span style="color:#F59E0B; font-weight: bold">●</span> Public 
                <span style="color:#8B5CF6; font-weight: bold">●</span> Private
            </h4>
        </div>
    '''
    metro_manila_map.get_root().html.add_child(folium.Element(title_html))
    
    # Create feature groups for different layers
    universities_layer = folium.FeatureGroup(name="Universities")
    heatmap_layer = folium.FeatureGroup(name="Funding Heatmap")
    cluster_layer = MarkerCluster(name="University Clusters")
    
    # Add circle markers for each university
    for _, row in df.iterrows():
        # Set color based on university type
        color = '#F59E0B' if row['Type'] == 'Public' else '#8B5CF6'
        
        # Create detailed popup content
        popup_html = f"""
        <div style="font-family:Arial; min-width:200px">
            <h3 style="text-align:center">{row['University']}</h3>
            <hr style="margin:5px 0">
            <p><b>Research Funding:</b> ₱{row['Funding']} million</p>
            <p><b>Research Output:</b> {row['ResearchOutput']} papers</p>
            <p><b>Type:</b> {row['Type']} University</p>
            <p><b>City:</b> {row['City']}</p>
        </div>
        """
        
        # Add circle marker to universities layer
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=row['MarkerSize'],
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['ShortName']} - ₱{row['Funding']}M",
            weight=2,
            opacity=0.8
        ).add_to(universities_layer)
        
        # Add university name label
        folium.map.Marker(
            [row['Latitude'], row['Longitude']],
            icon=folium.DivIcon(
                icon_size=(150, 36),
                icon_anchor=(75, -5),
                html=f'<div style="font-size: 10pt; color:black; font-weight:bold; text-align:center">{row["ShortName"]}</div>'
            )
        ).add_to(universities_layer)
        
        # Add standard marker to cluster layer
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['ShortName']} - ₱{row['Funding']}M",
            icon=folium.Icon(
                color='orange' if row['Type'] == 'Public' else 'purple', 
                icon='university', 
                prefix='fa'
            )
        ).add_to(cluster_layer)
    
    # Add heatmap layer
    heat_data = [[row['Latitude'], row['Longitude'], row['Funding']] for _, row in df.iterrows()]
    HeatMap(
        heat_data, 
        radius=15, 
        blur=10, 
        gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 1: 'red'},
        name='Research Funding Intensity'
    ).add_to(heatmap_layer)
    
    # Add our layers to the map
    universities_layer.add_to(metro_manila_map)
    heatmap_layer.add_to(metro_manila_map)
    cluster_layer.add_to(metro_manila_map)
    
    # Add a custom legend
    legend_html = '''
    <div style="position: fixed; 
        bottom: 50px; left: 50px; 
        width: 220px; 
        height: auto; 
        border:2px solid grey; 
        z-index:9999; 
        font-size:14px;
        background-color:white; 
        padding: 10px; 
        border-radius: 5px;
        font-family: Arial">
        <p style="font-weight:bold; margin-bottom:8px">University Type</p>
        <div style="margin-bottom:5px">
            <span style="color:#F59E0B; font-size:16px">●</span> Public University
        </div>
        <div style="margin-bottom:10px">
            <span style="color:#8B5CF6; font-size:16px">●</span> Private University
        </div>
        <p style="font-weight:bold; margin-bottom:8px">Circle Size Legend</p>
        <div style="margin-bottom:5px">
            <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background-color:gray"></span> ₱50 million
        </div>
        <div style="margin-bottom:5px">
            <span style="display:inline-block; width:20px; height:20px; border-radius:50%; background-color:gray"></span> ₱250 million
        </div>
        <div style="margin-bottom:5px">
            <span style="display:inline-block; width:30px; height:30px; border-radius:50%; background-color:gray"></span> ₱500 million
        </div>
        <p style="font-size:10px; margin-top:10px">
            Source: DOST, CHED, and university reports (2024)
        </p>
    </div>
    '''
    metro_manila_map.get_root().html.add_child(folium.Element(legend_html))
    
    # Add layer control
    folium.LayerControl(position='topright').add_to(metro_manila_map)
    
    # Return the HTML representation of the map
    return metro_manila_map._repr_html_()
