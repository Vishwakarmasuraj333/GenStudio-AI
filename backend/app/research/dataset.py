"""
Standardized Academic Prompt Benchmark Dataset for Generative AI Research.
Curated across six challenging domain categories to test visual fidelity,
compositional understanding, text rendering, and motion dynamics.
"""
from typing import Optional, List, Dict, Any

BENCHMARK_PROMPTS = [
    # Category 1: Photorealism
    {
        "id": "PHOTO-001",
        "category": "photorealism",
        "prompt": "Macro close-up portrait of an elderly watchmaker with deep laugh lines, wearing round brass spectacles, examining intricate vintage watch gears under warm desk lamp illumination, 85mm lens, shallow depth of field.",
        "difficulty": "medium",
        "aspect_ratio": "1:1"
    },
    {
        "id": "PHOTO-002",
        "category": "photorealism",
        "prompt": "Morning dew drops resting on a vibrant emerald monstera leaf in a sunlit botanical glasshouse, crisp reflections, soft bokeh background, natural morning sunlight.",
        "difficulty": "low",
        "aspect_ratio": "16:9"
    },
    # Category 2: Spatial Composition & Object Relations
    {
        "id": "SPAT-001",
        "category": "spatial_composition",
        "prompt": "A transparent glass sphere resting on a worn wooden table to the left of a brass antique microscope, with a small green ceramic cup behind both objects, accurate cast shadows and light caustics.",
        "difficulty": "high",
        "aspect_ratio": "16:9"
    },
    {
        "id": "SPAT-002",
        "category": "spatial_composition",
        "prompt": "A modern minimalist living room: a blue velvet sofa positioned on the left facing a beige concrete coffee table, a tall potted fiddle-leaf fig tree in the far right corner, diffuse northern window light.",
        "difficulty": "medium",
        "aspect_ratio": "16:9"
    },
    # Category 3: Cinematic Aesthetics
    {
        "id": "CINE-001",
        "category": "cinematic",
        "prompt": "Cinematic wide shot of a solitary astronaut in an illuminated spacesuit standing on obsidian volcanic rock, gazing at an immense ringed gas giant rising over the horizon, teal and amber anamorphic color grading, lens flare.",
        "difficulty": "medium",
        "aspect_ratio": "16:9"
    },
    {
        "id": "CINE-002",
        "category": "cinematic",
        "prompt": "Rain-slicked neon street at midnight in Tokyo, vibrant reflections in puddles, steam rising from street drains, shallow focus, 35mm film grain, moody cyberpunk atmosphere.",
        "difficulty": "low",
        "aspect_ratio": "16:9"
    },
    # Category 4: Typography & Text Rendering
    {
        "id": "TYPO-001",
        "category": "typography",
        "prompt": "A rustic wooden coffee shop storefront sign with the clearly legible carved lettering 'GENSTUDIO COFFEE' in elegant serif typography, hanging above weathered oak doors, morning fog.",
        "difficulty": "very_high",
        "aspect_ratio": "1:1"
    },
    {
        "id": "TYPO-002",
        "category": "typography",
        "prompt": "A futuristic holographic billboard displaying the sharp text 'CYBER 2088' in glowing magenta and cyan letters against a dark skyscraper background.",
        "difficulty": "high",
        "aspect_ratio": "16:9"
    },
    # Category 5: Stylized Art & Complex Rendering
    {
        "id": "ART-001",
        "category": "artistic",
        "prompt": "Surreal oil painting of a mythical celestial library where books transform into luminous white birds flying towards a stained-glass vaulted ceiling, rich impasto brushwork, warm golden palette.",
        "difficulty": "medium",
        "aspect_ratio": "1:1"
    },
    {
        "id": "ART-002",
        "category": "artistic",
        "prompt": "Detailed concept art of an overgrown ancient stone temple submerged in crystal-clear turquoise jungle waters, schools of glowing bioluminescent fish swimming through carved stone arches.",
        "difficulty": "medium",
        "aspect_ratio": "16:9"
    },
    # Category 6: Motion Dynamics (For Video Synthesis)
    {
        "id": "VID-001",
        "category": "motion_dynamics",
        "prompt": "Slow-motion drone flight descending through misty mountain pines towards a roaring waterfall at golden hour, droplets spraying towards the camera lens.",
        "difficulty": "high",
        "aspect_ratio": "16:9"
    },
    {
        "id": "VID-002",
        "category": "motion_dynamics",
        "prompt": "A sleek silver sports car accelerating down a winding coastal highway at dusk, smooth tracking camera following alongside, ocean waves crashing below.",
        "difficulty": "high",
        "aspect_ratio": "16:9"
    }
]

def get_benchmark_prompts(category: Optional[str] = "all", limit: int = 10):
    if category and category != "all":
        filtered = [p for p in BENCHMARK_PROMPTS if p["category"] == category]
    else:
        filtered = BENCHMARK_PROMPTS
    return filtered[:limit]
