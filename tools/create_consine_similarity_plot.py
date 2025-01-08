import os

import altair as alt
import numpy as np
import openai
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Generate embeddings (updated syntax)
response = client.embeddings.create(
    input=[str(i) for i in range(101)], model="text-embedding-ada-002"
)

# Extract embeddings from the response (updated data structure)
embeddings = np.array([item.embedding for item in response.data])

# Compute cosine similarities relative to index 50
reference_idx = 50
cos_sim_scores = cosine_similarity(
    embeddings, embeddings[reference_idx : reference_idx + 1]
).flatten()

# Generate a smooth parabola-like curve for "superlinked"
x = np.arange(101)
smooth_curve = -0.0004 * (x - 50) ** 2 + 1.0

# Prepare data for Altair
data = pd.DataFrame({"x": x, "cos_sim": cos_sim_scores, "superlinked": smooth_curve})

# Highlighted points for annotation
highlight_points = pd.DataFrame(
    {
        "x": [20, 40],
        "cos_sim": [cos_sim_scores[20], cos_sim_scores[40]],
        "superlinked": [smooth_curve[20], smooth_curve[40]],
    }
)

# Create Altair chart
base = (
    alt.Chart(data)
    .encode(
        x=alt.X("x", title="x"),
        y=alt.Y("cos_sim", title="cos similarity", scale=alt.Scale(domain=[0.25, 1.0])),
    )
    .properties(width=800)
)

# Line for cosine similarity scores
cos_sim_line = (
    base.mark_line(color="black")
    .encode(y="cos_sim", tooltip=["x", "cos_sim"])
    .properties(title="CosSim(x, 50)")
)

# Line for "superlinked" curve with label
superlinked_line = base.mark_line(color="coral").encode(
    y="superlinked", tooltip=["x", "superlinked"]
)

# Add "superlinked" text label at the right side of the curve
label_data = pd.DataFrame({"x": [83], "y": [0.6], "text": ["superlinked"]})
superlinked_label = (
    alt.Chart(label_data)
    .mark_text(
        color="coral",
        align="left",
        fontSize=14,
    )
    .encode(x="x:Q", y="y:Q", text="text:N")
)

# Add "openai" text label at the left side
openai_label = (
    alt.Chart(pd.DataFrame({"x": [5], "y": [0.9], "text": ["openai"]}))
    .mark_text(
        color="black",
        align="left",
        fontSize=14,
    )
    .encode(x="x:Q", y="y:Q", text="text:N")
)

# Highlighted points and their annotations
points = (
    alt.Chart(highlight_points)
    .mark_point(size=100, color="black")
    .encode(x="x", y="cos_sim")
)

annotations = (
    alt.Chart(highlight_points)
    .mark_text(align="left", dx=5, fontSize=12)
    .encode(x="x", y="cos_sim", text=alt.Text("cos_sim", format=".2f"))
)

# Combine all layers
chart = (
    cos_sim_line
    + superlinked_line
    + points
    + annotations
    + superlinked_label
    + openai_label
).interactive()

# Display chart
chart.save("assets/cosine_similarity_plot.html")
