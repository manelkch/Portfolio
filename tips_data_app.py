
def page_content_tips():    
    import streamlit as st
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import bokeh
    from bokeh.plotting import figure
    from bokeh.palettes import magma
    from bokeh.layouts import row, column
    from bokeh.models import HoverTool
    from bokeh.models import Button, CustomJS, CheckboxGroup, RadioGroup, Slider
    import plotly.express as px


    st.title("Tips Data")
    data = pd.read_csv('data/tips.csv', delimiter=',')
    data

    st.write("Seaborn : ")
    plt.title('Title using Matplotlib Function')
    sns.lineplot(x="sex", y="total_bill", data=data)
    st.pyplot(plt)

    plt.clf()
    st.write("Scatter Plot : ")

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    sns.scatterplot(ax=axes[0], x='day', y='tip', data=data)
    axes[0].set_title("Tip per Day")

    sns.scatterplot(ax=axes[1], x='day', y='tip', data=data,hue='sex')
    axes[1].set_title("Tip per Day by Gender")

    plt.tight_layout()
    st.pyplot(fig)

    plt.clf()
    st.write("Line Plot : ")
    sns.lineplot(x='day', y='tip', data=data)
    st.pyplot(plt)

    plt.clf()
    sns.lineplot(data=data.drop(['total_bill'], axis=1))
    st.pyplot(plt)

    st.write("Bar plot : ")
    plt.clf()
    sns.barplot(x='day',y='tip', data=data, hue='sex')
    st.pyplot(plt)

    st.write("Hist plot : ")
    plt.clf()
    sns.histplot(x='total_bill', data=data, kde=True, hue='sex')
    st.pyplot(plt)

    st.write("Bokeh : ")
    st.write("Scatter plot and Line Chart : ")

    graph1 = figure(title = "Bokeh Scatter Graph",width=400, height=400)
    color = magma(256)
    graph1.scatter(data['total_bill'], data['tip'], color=color)

    graph2 = figure(title = "Bokeh Bar Chart",width=400, height=400)
    df = data['tip'].value_counts()
    graph2.line(df, data['tip'])

    layout = row(graph1, graph2)
    st.bokeh_chart(layout)

    st.write("Bar Chart : ")
    graph = figure(title = "Bokeh Vertical Bar Chart", width=500, height=500)
    graph.vbar(data['total_bill'], top=data['tip'])
    st.bokeh_chart(graph)

    st.write("Interactive Data Visualization : ")

    it_graph1 = figure(title = "Bokeh Bar Chart", width=400, height=400)
    it_graph1.vbar(data['total_bill'], top=data['tip'],
            legend_label = "Bill VS Tips", color='green')
    it_graph1.vbar(data['tip'], top=data['size'],
            legend_label = "Tips VS Size", color='red')
    it_graph1.legend.click_policy = "hide"

    it_graph2 = figure(title = "Bokeh Bar Chart", width=400, height=400)
    it_graph2.vbar(data["total_bill"], top = data['tip'], legend_label = "Bill VS Tips",color = "green")
    it_graph2.vbar(data["tip"], top = data['size'], legend_label = "Tips VS Size",color = "red")
    it_graph2.legend.click_policy = "hide"
    it_graph2.add_tools(HoverTool())

    layout = row(it_graph1, it_graph2)
    st.bokeh_chart(layout)

    st.write("Create a button : ")
    button = Button(label="Foo", button_type="primary")
    callback = CustomJS(args=dict(button=button), code="""
        button.label = 'Bar';
    """)
    button.js_on_event("button_click", callback)
    st.bokeh_chart(button)

    st.write("Create a button widget : ")

    button = Button(label="GFG")
    
    # Add JavaScript callback on button click
    button.js_on_click(CustomJS(code="console.log('button: click!', this.toString())"))
    
    # Labels for checkbox and radio buttons
    L = ["First", "Second", "Third"]
    
    # Create a CheckboxGroup widget
    checkbox_group = CheckboxGroup(labels=L, active=[0, 2])
    
    # Add JavaScript callback on CheckboxGroup change
    checkbox_group.js_on_change('active', CustomJS(code="""
        console.log('checkbox_group: active=' + this.active, this.toString())
    """))
    
    # Create a RadioGroup widget
    radio_group = RadioGroup(labels=L, active=1)
    
    # Add JavaScript callback on RadioGroup change
    radio_group.js_on_change('active', CustomJS(code="""
        console.log('radio_group: active=' + this.active, this.toString())
    """))
    
    # Display the widgets
    widgets = column(button, checkbox_group, radio_group)
    st.bokeh_chart(widgets)

    st.write("Sliders : ")
    slider = Slider(start=1, end=20, value=1, step=2, title="Slider")
    slider.js_on_change("value", CustomJS(code="""
        console.log('slider: value=' + this.value, this.toString())
    """))
    st.bokeh_chart(slider)

    st.write("Plotly : ")

    fig1 = px.scatter(data, x="day", y="tip", color='sex')
    fig2 = px.line(data, y='tip', color='sex')
    fig3 = px.bar(data, x='day', y='tip', color='sex')
    fig4 = px.histogram(data, x='total_bill', color='sex')

    st.write("Scatter Chart ")
    st.plotly_chart(fig1)
    st.write("Line Chart ")
    st.plotly_chart(fig2)
    st.write("Bar Chart ")
    st.plotly_chart(fig3)
    st.write("Histogram Chart ")
    st.plotly_chart(fig4)
