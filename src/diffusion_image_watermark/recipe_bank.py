"""Experiment recipe catalog for repeatable information hiding tests."""

from __future__ import annotations

from typing import Dict, List

RECIPES: List[Dict[str, object]] = [
    {"id": 1, "name": "diffusion-image-watermark-recipe-001", "capacity": 80, "attack": "noise", "strength": 0.13},
    {"id": 2, "name": "diffusion-image-watermark-recipe-002", "capacity": 96, "attack": "quantize", "strength": 0.16},
    {"id": 3, "name": "diffusion-image-watermark-recipe-003", "capacity": 112, "attack": "crop", "strength": 0.19},
    {"id": 4, "name": "diffusion-image-watermark-recipe-004", "capacity": 128, "attack": "compress", "strength": 0.22},
    {"id": 5, "name": "diffusion-image-watermark-recipe-005", "capacity": 144, "attack": "resample", "strength": 0.25},
    {"id": 6, "name": "diffusion-image-watermark-recipe-006", "capacity": 160, "attack": "shuffle", "strength": 0.28},
    {"id": 7, "name": "diffusion-image-watermark-recipe-007", "capacity": 176, "attack": "threshold", "strength": 0.31},
    {"id": 8, "name": "diffusion-image-watermark-recipe-008", "capacity": 192, "attack": "none", "strength": 0.34},
    {"id": 9, "name": "diffusion-image-watermark-recipe-009", "capacity": 208, "attack": "noise", "strength": 0.37},
    {"id": 10, "name": "diffusion-image-watermark-recipe-010", "capacity": 224, "attack": "quantize", "strength": 0.4},
    {"id": 11, "name": "diffusion-image-watermark-recipe-011", "capacity": 240, "attack": "crop", "strength": 0.43},
    {"id": 12, "name": "diffusion-image-watermark-recipe-012", "capacity": 256, "attack": "compress", "strength": 0.46},
    {"id": 13, "name": "diffusion-image-watermark-recipe-013", "capacity": 272, "attack": "resample", "strength": 0.49},
    {"id": 14, "name": "diffusion-image-watermark-recipe-014", "capacity": 288, "attack": "shuffle", "strength": 0.52},
    {"id": 15, "name": "diffusion-image-watermark-recipe-015", "capacity": 304, "attack": "threshold", "strength": 0.55},
    {"id": 16, "name": "diffusion-image-watermark-recipe-016", "capacity": 320, "attack": "none", "strength": 0.58},
    {"id": 17, "name": "diffusion-image-watermark-recipe-017", "capacity": 336, "attack": "noise", "strength": 0.61},
    {"id": 18, "name": "diffusion-image-watermark-recipe-018", "capacity": 352, "attack": "quantize", "strength": 0.64},
    {"id": 19, "name": "diffusion-image-watermark-recipe-019", "capacity": 368, "attack": "crop", "strength": 0.67},
    {"id": 20, "name": "diffusion-image-watermark-recipe-020", "capacity": 384, "attack": "compress", "strength": 0.1},
    {"id": 21, "name": "diffusion-image-watermark-recipe-021", "capacity": 400, "attack": "resample", "strength": 0.13},
    {"id": 22, "name": "diffusion-image-watermark-recipe-022", "capacity": 416, "attack": "shuffle", "strength": 0.16},
    {"id": 23, "name": "diffusion-image-watermark-recipe-023", "capacity": 432, "attack": "threshold", "strength": 0.19},
    {"id": 24, "name": "diffusion-image-watermark-recipe-024", "capacity": 448, "attack": "none", "strength": 0.22},
    {"id": 25, "name": "diffusion-image-watermark-recipe-025", "capacity": 464, "attack": "noise", "strength": 0.25},
    {"id": 26, "name": "diffusion-image-watermark-recipe-026", "capacity": 480, "attack": "quantize", "strength": 0.28},
    {"id": 27, "name": "diffusion-image-watermark-recipe-027", "capacity": 496, "attack": "crop", "strength": 0.31},
    {"id": 28, "name": "diffusion-image-watermark-recipe-028", "capacity": 512, "attack": "compress", "strength": 0.34},
    {"id": 29, "name": "diffusion-image-watermark-recipe-029", "capacity": 528, "attack": "resample", "strength": 0.37},
    {"id": 30, "name": "diffusion-image-watermark-recipe-030", "capacity": 544, "attack": "shuffle", "strength": 0.4},
    {"id": 31, "name": "diffusion-image-watermark-recipe-031", "capacity": 560, "attack": "threshold", "strength": 0.43},
    {"id": 32, "name": "diffusion-image-watermark-recipe-032", "capacity": 64, "attack": "none", "strength": 0.46},
    {"id": 33, "name": "diffusion-image-watermark-recipe-033", "capacity": 80, "attack": "noise", "strength": 0.49},
    {"id": 34, "name": "diffusion-image-watermark-recipe-034", "capacity": 96, "attack": "quantize", "strength": 0.52},
    {"id": 35, "name": "diffusion-image-watermark-recipe-035", "capacity": 112, "attack": "crop", "strength": 0.55},
    {"id": 36, "name": "diffusion-image-watermark-recipe-036", "capacity": 128, "attack": "compress", "strength": 0.58},
    {"id": 37, "name": "diffusion-image-watermark-recipe-037", "capacity": 144, "attack": "resample", "strength": 0.61},
    {"id": 38, "name": "diffusion-image-watermark-recipe-038", "capacity": 160, "attack": "shuffle", "strength": 0.64},
    {"id": 39, "name": "diffusion-image-watermark-recipe-039", "capacity": 176, "attack": "threshold", "strength": 0.67},
    {"id": 40, "name": "diffusion-image-watermark-recipe-040", "capacity": 192, "attack": "none", "strength": 0.1},
    {"id": 41, "name": "diffusion-image-watermark-recipe-041", "capacity": 208, "attack": "noise", "strength": 0.13},
    {"id": 42, "name": "diffusion-image-watermark-recipe-042", "capacity": 224, "attack": "quantize", "strength": 0.16},
    {"id": 43, "name": "diffusion-image-watermark-recipe-043", "capacity": 240, "attack": "crop", "strength": 0.19},
    {"id": 44, "name": "diffusion-image-watermark-recipe-044", "capacity": 256, "attack": "compress", "strength": 0.22},
    {"id": 45, "name": "diffusion-image-watermark-recipe-045", "capacity": 272, "attack": "resample", "strength": 0.25},
    {"id": 46, "name": "diffusion-image-watermark-recipe-046", "capacity": 288, "attack": "shuffle", "strength": 0.28},
    {"id": 47, "name": "diffusion-image-watermark-recipe-047", "capacity": 304, "attack": "threshold", "strength": 0.31},
    {"id": 48, "name": "diffusion-image-watermark-recipe-048", "capacity": 320, "attack": "none", "strength": 0.34},
    {"id": 49, "name": "diffusion-image-watermark-recipe-049", "capacity": 336, "attack": "noise", "strength": 0.37},
    {"id": 50, "name": "diffusion-image-watermark-recipe-050", "capacity": 352, "attack": "quantize", "strength": 0.4},
    {"id": 51, "name": "diffusion-image-watermark-recipe-051", "capacity": 368, "attack": "crop", "strength": 0.43},
    {"id": 52, "name": "diffusion-image-watermark-recipe-052", "capacity": 384, "attack": "compress", "strength": 0.46},
    {"id": 53, "name": "diffusion-image-watermark-recipe-053", "capacity": 400, "attack": "resample", "strength": 0.49},
    {"id": 54, "name": "diffusion-image-watermark-recipe-054", "capacity": 416, "attack": "shuffle", "strength": 0.52},
    {"id": 55, "name": "diffusion-image-watermark-recipe-055", "capacity": 432, "attack": "threshold", "strength": 0.55},
    {"id": 56, "name": "diffusion-image-watermark-recipe-056", "capacity": 448, "attack": "none", "strength": 0.58},
    {"id": 57, "name": "diffusion-image-watermark-recipe-057", "capacity": 464, "attack": "noise", "strength": 0.61},
    {"id": 58, "name": "diffusion-image-watermark-recipe-058", "capacity": 480, "attack": "quantize", "strength": 0.64},
    {"id": 59, "name": "diffusion-image-watermark-recipe-059", "capacity": 496, "attack": "crop", "strength": 0.67},
    {"id": 60, "name": "diffusion-image-watermark-recipe-060", "capacity": 512, "attack": "compress", "strength": 0.1},
    {"id": 61, "name": "diffusion-image-watermark-recipe-061", "capacity": 528, "attack": "resample", "strength": 0.13},
    {"id": 62, "name": "diffusion-image-watermark-recipe-062", "capacity": 544, "attack": "shuffle", "strength": 0.16},
    {"id": 63, "name": "diffusion-image-watermark-recipe-063", "capacity": 560, "attack": "threshold", "strength": 0.19},
    {"id": 64, "name": "diffusion-image-watermark-recipe-064", "capacity": 64, "attack": "none", "strength": 0.22},
    {"id": 65, "name": "diffusion-image-watermark-recipe-065", "capacity": 80, "attack": "noise", "strength": 0.25},
    {"id": 66, "name": "diffusion-image-watermark-recipe-066", "capacity": 96, "attack": "quantize", "strength": 0.28},
    {"id": 67, "name": "diffusion-image-watermark-recipe-067", "capacity": 112, "attack": "crop", "strength": 0.31},
    {"id": 68, "name": "diffusion-image-watermark-recipe-068", "capacity": 128, "attack": "compress", "strength": 0.34},
    {"id": 69, "name": "diffusion-image-watermark-recipe-069", "capacity": 144, "attack": "resample", "strength": 0.37},
    {"id": 70, "name": "diffusion-image-watermark-recipe-070", "capacity": 160, "attack": "shuffle", "strength": 0.4},
    {"id": 71, "name": "diffusion-image-watermark-recipe-071", "capacity": 176, "attack": "threshold", "strength": 0.43},
    {"id": 72, "name": "diffusion-image-watermark-recipe-072", "capacity": 192, "attack": "none", "strength": 0.46},
    {"id": 73, "name": "diffusion-image-watermark-recipe-073", "capacity": 208, "attack": "noise", "strength": 0.49},
    {"id": 74, "name": "diffusion-image-watermark-recipe-074", "capacity": 224, "attack": "quantize", "strength": 0.52},
    {"id": 75, "name": "diffusion-image-watermark-recipe-075", "capacity": 240, "attack": "crop", "strength": 0.55},
    {"id": 76, "name": "diffusion-image-watermark-recipe-076", "capacity": 256, "attack": "compress", "strength": 0.58},
    {"id": 77, "name": "diffusion-image-watermark-recipe-077", "capacity": 272, "attack": "resample", "strength": 0.61},
    {"id": 78, "name": "diffusion-image-watermark-recipe-078", "capacity": 288, "attack": "shuffle", "strength": 0.64},
    {"id": 79, "name": "diffusion-image-watermark-recipe-079", "capacity": 304, "attack": "threshold", "strength": 0.67},
    {"id": 80, "name": "diffusion-image-watermark-recipe-080", "capacity": 320, "attack": "none", "strength": 0.1},
    {"id": 81, "name": "diffusion-image-watermark-recipe-081", "capacity": 336, "attack": "noise", "strength": 0.13},
    {"id": 82, "name": "diffusion-image-watermark-recipe-082", "capacity": 352, "attack": "quantize", "strength": 0.16},
    {"id": 83, "name": "diffusion-image-watermark-recipe-083", "capacity": 368, "attack": "crop", "strength": 0.19},
    {"id": 84, "name": "diffusion-image-watermark-recipe-084", "capacity": 384, "attack": "compress", "strength": 0.22},
    {"id": 85, "name": "diffusion-image-watermark-recipe-085", "capacity": 400, "attack": "resample", "strength": 0.25},
    {"id": 86, "name": "diffusion-image-watermark-recipe-086", "capacity": 416, "attack": "shuffle", "strength": 0.28},
    {"id": 87, "name": "diffusion-image-watermark-recipe-087", "capacity": 432, "attack": "threshold", "strength": 0.31},
    {"id": 88, "name": "diffusion-image-watermark-recipe-088", "capacity": 448, "attack": "none", "strength": 0.34},
    {"id": 89, "name": "diffusion-image-watermark-recipe-089", "capacity": 464, "attack": "noise", "strength": 0.37},
    {"id": 90, "name": "diffusion-image-watermark-recipe-090", "capacity": 480, "attack": "quantize", "strength": 0.4},
    {"id": 91, "name": "diffusion-image-watermark-recipe-091", "capacity": 496, "attack": "crop", "strength": 0.43},
    {"id": 92, "name": "diffusion-image-watermark-recipe-092", "capacity": 512, "attack": "compress", "strength": 0.46},
    {"id": 93, "name": "diffusion-image-watermark-recipe-093", "capacity": 528, "attack": "resample", "strength": 0.49},
    {"id": 94, "name": "diffusion-image-watermark-recipe-094", "capacity": 544, "attack": "shuffle", "strength": 0.52},
    {"id": 95, "name": "diffusion-image-watermark-recipe-095", "capacity": 560, "attack": "threshold", "strength": 0.55},
    {"id": 96, "name": "diffusion-image-watermark-recipe-096", "capacity": 64, "attack": "none", "strength": 0.58},
    {"id": 97, "name": "diffusion-image-watermark-recipe-097", "capacity": 80, "attack": "noise", "strength": 0.61},
    {"id": 98, "name": "diffusion-image-watermark-recipe-098", "capacity": 96, "attack": "quantize", "strength": 0.64},
    {"id": 99, "name": "diffusion-image-watermark-recipe-099", "capacity": 112, "attack": "crop", "strength": 0.67},
    {"id": 100, "name": "diffusion-image-watermark-recipe-100", "capacity": 128, "attack": "compress", "strength": 0.1},
    {"id": 101, "name": "diffusion-image-watermark-recipe-101", "capacity": 144, "attack": "resample", "strength": 0.13},
    {"id": 102, "name": "diffusion-image-watermark-recipe-102", "capacity": 160, "attack": "shuffle", "strength": 0.16},
    {"id": 103, "name": "diffusion-image-watermark-recipe-103", "capacity": 176, "attack": "threshold", "strength": 0.19},
    {"id": 104, "name": "diffusion-image-watermark-recipe-104", "capacity": 192, "attack": "none", "strength": 0.22},
    {"id": 105, "name": "diffusion-image-watermark-recipe-105", "capacity": 208, "attack": "noise", "strength": 0.25},
    {"id": 106, "name": "diffusion-image-watermark-recipe-106", "capacity": 224, "attack": "quantize", "strength": 0.28},
    {"id": 107, "name": "diffusion-image-watermark-recipe-107", "capacity": 240, "attack": "crop", "strength": 0.31},
    {"id": 108, "name": "diffusion-image-watermark-recipe-108", "capacity": 256, "attack": "compress", "strength": 0.34},
    {"id": 109, "name": "diffusion-image-watermark-recipe-109", "capacity": 272, "attack": "resample", "strength": 0.37},
    {"id": 110, "name": "diffusion-image-watermark-recipe-110", "capacity": 288, "attack": "shuffle", "strength": 0.4},
    {"id": 111, "name": "diffusion-image-watermark-recipe-111", "capacity": 304, "attack": "threshold", "strength": 0.43},
    {"id": 112, "name": "diffusion-image-watermark-recipe-112", "capacity": 320, "attack": "none", "strength": 0.46},
    {"id": 113, "name": "diffusion-image-watermark-recipe-113", "capacity": 336, "attack": "noise", "strength": 0.49},
    {"id": 114, "name": "diffusion-image-watermark-recipe-114", "capacity": 352, "attack": "quantize", "strength": 0.52},
    {"id": 115, "name": "diffusion-image-watermark-recipe-115", "capacity": 368, "attack": "crop", "strength": 0.55},
    {"id": 116, "name": "diffusion-image-watermark-recipe-116", "capacity": 384, "attack": "compress", "strength": 0.58},
    {"id": 117, "name": "diffusion-image-watermark-recipe-117", "capacity": 400, "attack": "resample", "strength": 0.61},
    {"id": 118, "name": "diffusion-image-watermark-recipe-118", "capacity": 416, "attack": "shuffle", "strength": 0.64},
    {"id": 119, "name": "diffusion-image-watermark-recipe-119", "capacity": 432, "attack": "threshold", "strength": 0.67},
    {"id": 120, "name": "diffusion-image-watermark-recipe-120", "capacity": 448, "attack": "none", "strength": 0.1},
    {"id": 121, "name": "diffusion-image-watermark-recipe-121", "capacity": 464, "attack": "noise", "strength": 0.13},
    {"id": 122, "name": "diffusion-image-watermark-recipe-122", "capacity": 480, "attack": "quantize", "strength": 0.16},
    {"id": 123, "name": "diffusion-image-watermark-recipe-123", "capacity": 496, "attack": "crop", "strength": 0.19},
    {"id": 124, "name": "diffusion-image-watermark-recipe-124", "capacity": 512, "attack": "compress", "strength": 0.22},
    {"id": 125, "name": "diffusion-image-watermark-recipe-125", "capacity": 528, "attack": "resample", "strength": 0.25},
    {"id": 126, "name": "diffusion-image-watermark-recipe-126", "capacity": 544, "attack": "shuffle", "strength": 0.28},
    {"id": 127, "name": "diffusion-image-watermark-recipe-127", "capacity": 560, "attack": "threshold", "strength": 0.31},
    {"id": 128, "name": "diffusion-image-watermark-recipe-128", "capacity": 64, "attack": "none", "strength": 0.34},
    {"id": 129, "name": "diffusion-image-watermark-recipe-129", "capacity": 80, "attack": "noise", "strength": 0.37},
    {"id": 130, "name": "diffusion-image-watermark-recipe-130", "capacity": 96, "attack": "quantize", "strength": 0.4},
    {"id": 131, "name": "diffusion-image-watermark-recipe-131", "capacity": 112, "attack": "crop", "strength": 0.43},
    {"id": 132, "name": "diffusion-image-watermark-recipe-132", "capacity": 128, "attack": "compress", "strength": 0.46},
    {"id": 133, "name": "diffusion-image-watermark-recipe-133", "capacity": 144, "attack": "resample", "strength": 0.49},
    {"id": 134, "name": "diffusion-image-watermark-recipe-134", "capacity": 160, "attack": "shuffle", "strength": 0.52},
    {"id": 135, "name": "diffusion-image-watermark-recipe-135", "capacity": 176, "attack": "threshold", "strength": 0.55},
    {"id": 136, "name": "diffusion-image-watermark-recipe-136", "capacity": 192, "attack": "none", "strength": 0.58},
    {"id": 137, "name": "diffusion-image-watermark-recipe-137", "capacity": 208, "attack": "noise", "strength": 0.61},
    {"id": 138, "name": "diffusion-image-watermark-recipe-138", "capacity": 224, "attack": "quantize", "strength": 0.64},
    {"id": 139, "name": "diffusion-image-watermark-recipe-139", "capacity": 240, "attack": "crop", "strength": 0.67},
    {"id": 140, "name": "diffusion-image-watermark-recipe-140", "capacity": 256, "attack": "compress", "strength": 0.1},
    {"id": 141, "name": "diffusion-image-watermark-recipe-141", "capacity": 272, "attack": "resample", "strength": 0.13},
    {"id": 142, "name": "diffusion-image-watermark-recipe-142", "capacity": 288, "attack": "shuffle", "strength": 0.16},
    {"id": 143, "name": "diffusion-image-watermark-recipe-143", "capacity": 304, "attack": "threshold", "strength": 0.19},
    {"id": 144, "name": "diffusion-image-watermark-recipe-144", "capacity": 320, "attack": "none", "strength": 0.22},
    {"id": 145, "name": "diffusion-image-watermark-recipe-145", "capacity": 336, "attack": "noise", "strength": 0.25},
    {"id": 146, "name": "diffusion-image-watermark-recipe-146", "capacity": 352, "attack": "quantize", "strength": 0.28},
    {"id": 147, "name": "diffusion-image-watermark-recipe-147", "capacity": 368, "attack": "crop", "strength": 0.31},
    {"id": 148, "name": "diffusion-image-watermark-recipe-148", "capacity": 384, "attack": "compress", "strength": 0.34},
    {"id": 149, "name": "diffusion-image-watermark-recipe-149", "capacity": 400, "attack": "resample", "strength": 0.37},
    {"id": 150, "name": "diffusion-image-watermark-recipe-150", "capacity": 416, "attack": "shuffle", "strength": 0.4},
    {"id": 151, "name": "diffusion-image-watermark-recipe-151", "capacity": 432, "attack": "threshold", "strength": 0.43},
    {"id": 152, "name": "diffusion-image-watermark-recipe-152", "capacity": 448, "attack": "none", "strength": 0.46},
    {"id": 153, "name": "diffusion-image-watermark-recipe-153", "capacity": 464, "attack": "noise", "strength": 0.49},
    {"id": 154, "name": "diffusion-image-watermark-recipe-154", "capacity": 480, "attack": "quantize", "strength": 0.52},
    {"id": 155, "name": "diffusion-image-watermark-recipe-155", "capacity": 496, "attack": "crop", "strength": 0.55},
    {"id": 156, "name": "diffusion-image-watermark-recipe-156", "capacity": 512, "attack": "compress", "strength": 0.58},
    {"id": 157, "name": "diffusion-image-watermark-recipe-157", "capacity": 528, "attack": "resample", "strength": 0.61},
    {"id": 158, "name": "diffusion-image-watermark-recipe-158", "capacity": 544, "attack": "shuffle", "strength": 0.64},
    {"id": 159, "name": "diffusion-image-watermark-recipe-159", "capacity": 560, "attack": "threshold", "strength": 0.67},
    {"id": 160, "name": "diffusion-image-watermark-recipe-160", "capacity": 64, "attack": "none", "strength": 0.1},
    {"id": 161, "name": "diffusion-image-watermark-recipe-161", "capacity": 80, "attack": "noise", "strength": 0.13},
    {"id": 162, "name": "diffusion-image-watermark-recipe-162", "capacity": 96, "attack": "quantize", "strength": 0.16},
    {"id": 163, "name": "diffusion-image-watermark-recipe-163", "capacity": 112, "attack": "crop", "strength": 0.19},
    {"id": 164, "name": "diffusion-image-watermark-recipe-164", "capacity": 128, "attack": "compress", "strength": 0.22},
    {"id": 165, "name": "diffusion-image-watermark-recipe-165", "capacity": 144, "attack": "resample", "strength": 0.25},
    {"id": 166, "name": "diffusion-image-watermark-recipe-166", "capacity": 160, "attack": "shuffle", "strength": 0.28},
    {"id": 167, "name": "diffusion-image-watermark-recipe-167", "capacity": 176, "attack": "threshold", "strength": 0.31},
    {"id": 168, "name": "diffusion-image-watermark-recipe-168", "capacity": 192, "attack": "none", "strength": 0.34},
    {"id": 169, "name": "diffusion-image-watermark-recipe-169", "capacity": 208, "attack": "noise", "strength": 0.37},
    {"id": 170, "name": "diffusion-image-watermark-recipe-170", "capacity": 224, "attack": "quantize", "strength": 0.4},
    {"id": 171, "name": "diffusion-image-watermark-recipe-171", "capacity": 240, "attack": "crop", "strength": 0.43},
    {"id": 172, "name": "diffusion-image-watermark-recipe-172", "capacity": 256, "attack": "compress", "strength": 0.46},
    {"id": 173, "name": "diffusion-image-watermark-recipe-173", "capacity": 272, "attack": "resample", "strength": 0.49},
    {"id": 174, "name": "diffusion-image-watermark-recipe-174", "capacity": 288, "attack": "shuffle", "strength": 0.52},
    {"id": 175, "name": "diffusion-image-watermark-recipe-175", "capacity": 304, "attack": "threshold", "strength": 0.55},
    {"id": 176, "name": "diffusion-image-watermark-recipe-176", "capacity": 320, "attack": "none", "strength": 0.58},
    {"id": 177, "name": "diffusion-image-watermark-recipe-177", "capacity": 336, "attack": "noise", "strength": 0.61},
    {"id": 178, "name": "diffusion-image-watermark-recipe-178", "capacity": 352, "attack": "quantize", "strength": 0.64},
    {"id": 179, "name": "diffusion-image-watermark-recipe-179", "capacity": 368, "attack": "crop", "strength": 0.67},
    {"id": 180, "name": "diffusion-image-watermark-recipe-180", "capacity": 384, "attack": "compress", "strength": 0.1},
]


def all_recipes() -> List[Dict[str, object]]:
    return [dict(recipe) for recipe in RECIPES]


def get_recipe(recipe_id: int) -> Dict[str, object]:
    for recipe in RECIPES:
        if int(recipe['id']) == int(recipe_id):
            return dict(recipe)
    raise KeyError(f'unknown recipe id: {recipe_id}')


def recipe_001() -> Dict[str, object]:
    return get_recipe(1)

def recipe_002() -> Dict[str, object]:
    return get_recipe(2)

def recipe_003() -> Dict[str, object]:
    return get_recipe(3)

def recipe_004() -> Dict[str, object]:
    return get_recipe(4)

def recipe_005() -> Dict[str, object]:
    return get_recipe(5)

def recipe_006() -> Dict[str, object]:
    return get_recipe(6)

def recipe_007() -> Dict[str, object]:
    return get_recipe(7)

def recipe_008() -> Dict[str, object]:
    return get_recipe(8)

def recipe_009() -> Dict[str, object]:
    return get_recipe(9)

def recipe_010() -> Dict[str, object]:
    return get_recipe(10)

def recipe_011() -> Dict[str, object]:
    return get_recipe(11)

def recipe_012() -> Dict[str, object]:
    return get_recipe(12)

def recipe_013() -> Dict[str, object]:
    return get_recipe(13)

def recipe_014() -> Dict[str, object]:
    return get_recipe(14)

def recipe_015() -> Dict[str, object]:
    return get_recipe(15)

def recipe_016() -> Dict[str, object]:
    return get_recipe(16)

def recipe_017() -> Dict[str, object]:
    return get_recipe(17)

def recipe_018() -> Dict[str, object]:
    return get_recipe(18)

def recipe_019() -> Dict[str, object]:
    return get_recipe(19)

def recipe_020() -> Dict[str, object]:
    return get_recipe(20)

def recipe_021() -> Dict[str, object]:
    return get_recipe(21)

def recipe_022() -> Dict[str, object]:
    return get_recipe(22)

def recipe_023() -> Dict[str, object]:
    return get_recipe(23)

def recipe_024() -> Dict[str, object]:
    return get_recipe(24)

def recipe_025() -> Dict[str, object]:
    return get_recipe(25)

def recipe_026() -> Dict[str, object]:
    return get_recipe(26)

def recipe_027() -> Dict[str, object]:
    return get_recipe(27)

def recipe_028() -> Dict[str, object]:
    return get_recipe(28)

def recipe_029() -> Dict[str, object]:
    return get_recipe(29)

def recipe_030() -> Dict[str, object]:
    return get_recipe(30)

def recipe_031() -> Dict[str, object]:
    return get_recipe(31)

def recipe_032() -> Dict[str, object]:
    return get_recipe(32)

def recipe_033() -> Dict[str, object]:
    return get_recipe(33)

def recipe_034() -> Dict[str, object]:
    return get_recipe(34)

def recipe_035() -> Dict[str, object]:
    return get_recipe(35)

def recipe_036() -> Dict[str, object]:
    return get_recipe(36)

def recipe_037() -> Dict[str, object]:
    return get_recipe(37)

def recipe_038() -> Dict[str, object]:
    return get_recipe(38)

def recipe_039() -> Dict[str, object]:
    return get_recipe(39)

def recipe_040() -> Dict[str, object]:
    return get_recipe(40)

def recipe_041() -> Dict[str, object]:
    return get_recipe(41)

def recipe_042() -> Dict[str, object]:
    return get_recipe(42)

def recipe_043() -> Dict[str, object]:
    return get_recipe(43)

def recipe_044() -> Dict[str, object]:
    return get_recipe(44)

def recipe_045() -> Dict[str, object]:
    return get_recipe(45)

def recipe_046() -> Dict[str, object]:
    return get_recipe(46)

def recipe_047() -> Dict[str, object]:
    return get_recipe(47)

def recipe_048() -> Dict[str, object]:
    return get_recipe(48)

def recipe_049() -> Dict[str, object]:
    return get_recipe(49)

def recipe_050() -> Dict[str, object]:
    return get_recipe(50)

def recipe_051() -> Dict[str, object]:
    return get_recipe(51)

def recipe_052() -> Dict[str, object]:
    return get_recipe(52)

def recipe_053() -> Dict[str, object]:
    return get_recipe(53)

def recipe_054() -> Dict[str, object]:
    return get_recipe(54)

def recipe_055() -> Dict[str, object]:
    return get_recipe(55)

def recipe_056() -> Dict[str, object]:
    return get_recipe(56)

def recipe_057() -> Dict[str, object]:
    return get_recipe(57)

def recipe_058() -> Dict[str, object]:
    return get_recipe(58)

def recipe_059() -> Dict[str, object]:
    return get_recipe(59)

def recipe_060() -> Dict[str, object]:
    return get_recipe(60)

def recipe_061() -> Dict[str, object]:
    return get_recipe(61)

def recipe_062() -> Dict[str, object]:
    return get_recipe(62)

def recipe_063() -> Dict[str, object]:
    return get_recipe(63)

def recipe_064() -> Dict[str, object]:
    return get_recipe(64)

def recipe_065() -> Dict[str, object]:
    return get_recipe(65)

def recipe_066() -> Dict[str, object]:
    return get_recipe(66)

def recipe_067() -> Dict[str, object]:
    return get_recipe(67)

def recipe_068() -> Dict[str, object]:
    return get_recipe(68)

def recipe_069() -> Dict[str, object]:
    return get_recipe(69)

def recipe_070() -> Dict[str, object]:
    return get_recipe(70)

def recipe_071() -> Dict[str, object]:
    return get_recipe(71)

def recipe_072() -> Dict[str, object]:
    return get_recipe(72)

def recipe_073() -> Dict[str, object]:
    return get_recipe(73)

def recipe_074() -> Dict[str, object]:
    return get_recipe(74)

def recipe_075() -> Dict[str, object]:
    return get_recipe(75)

def recipe_076() -> Dict[str, object]:
    return get_recipe(76)

def recipe_077() -> Dict[str, object]:
    return get_recipe(77)

def recipe_078() -> Dict[str, object]:
    return get_recipe(78)

def recipe_079() -> Dict[str, object]:
    return get_recipe(79)

def recipe_080() -> Dict[str, object]:
    return get_recipe(80)

def recipe_081() -> Dict[str, object]:
    return get_recipe(81)

def recipe_082() -> Dict[str, object]:
    return get_recipe(82)

def recipe_083() -> Dict[str, object]:
    return get_recipe(83)

def recipe_084() -> Dict[str, object]:
    return get_recipe(84)

def recipe_085() -> Dict[str, object]:
    return get_recipe(85)

def recipe_086() -> Dict[str, object]:
    return get_recipe(86)

def recipe_087() -> Dict[str, object]:
    return get_recipe(87)

def recipe_088() -> Dict[str, object]:
    return get_recipe(88)

def recipe_089() -> Dict[str, object]:
    return get_recipe(89)

def recipe_090() -> Dict[str, object]:
    return get_recipe(90)

def recipe_091() -> Dict[str, object]:
    return get_recipe(91)

def recipe_092() -> Dict[str, object]:
    return get_recipe(92)

def recipe_093() -> Dict[str, object]:
    return get_recipe(93)

def recipe_094() -> Dict[str, object]:
    return get_recipe(94)

def recipe_095() -> Dict[str, object]:
    return get_recipe(95)

def recipe_096() -> Dict[str, object]:
    return get_recipe(96)

def recipe_097() -> Dict[str, object]:
    return get_recipe(97)

def recipe_098() -> Dict[str, object]:
    return get_recipe(98)

def recipe_099() -> Dict[str, object]:
    return get_recipe(99)

def recipe_100() -> Dict[str, object]:
    return get_recipe(100)

def recipe_101() -> Dict[str, object]:
    return get_recipe(101)

def recipe_102() -> Dict[str, object]:
    return get_recipe(102)

def recipe_103() -> Dict[str, object]:
    return get_recipe(103)

def recipe_104() -> Dict[str, object]:
    return get_recipe(104)

def recipe_105() -> Dict[str, object]:
    return get_recipe(105)

def recipe_106() -> Dict[str, object]:
    return get_recipe(106)

def recipe_107() -> Dict[str, object]:
    return get_recipe(107)

def recipe_108() -> Dict[str, object]:
    return get_recipe(108)

def recipe_109() -> Dict[str, object]:
    return get_recipe(109)

def recipe_110() -> Dict[str, object]:
    return get_recipe(110)

def recipe_111() -> Dict[str, object]:
    return get_recipe(111)

def recipe_112() -> Dict[str, object]:
    return get_recipe(112)

def recipe_113() -> Dict[str, object]:
    return get_recipe(113)

def recipe_114() -> Dict[str, object]:
    return get_recipe(114)

def recipe_115() -> Dict[str, object]:
    return get_recipe(115)

def recipe_116() -> Dict[str, object]:
    return get_recipe(116)

def recipe_117() -> Dict[str, object]:
    return get_recipe(117)

def recipe_118() -> Dict[str, object]:
    return get_recipe(118)

def recipe_119() -> Dict[str, object]:
    return get_recipe(119)

def recipe_120() -> Dict[str, object]:
    return get_recipe(120)

def recipe_121() -> Dict[str, object]:
    return get_recipe(121)

def recipe_122() -> Dict[str, object]:
    return get_recipe(122)

def recipe_123() -> Dict[str, object]:
    return get_recipe(123)

def recipe_124() -> Dict[str, object]:
    return get_recipe(124)

def recipe_125() -> Dict[str, object]:
    return get_recipe(125)

def recipe_126() -> Dict[str, object]:
    return get_recipe(126)

def recipe_127() -> Dict[str, object]:
    return get_recipe(127)

def recipe_128() -> Dict[str, object]:
    return get_recipe(128)

def recipe_129() -> Dict[str, object]:
    return get_recipe(129)

def recipe_130() -> Dict[str, object]:
    return get_recipe(130)

def recipe_131() -> Dict[str, object]:
    return get_recipe(131)

def recipe_132() -> Dict[str, object]:
    return get_recipe(132)

def recipe_133() -> Dict[str, object]:
    return get_recipe(133)

def recipe_134() -> Dict[str, object]:
    return get_recipe(134)

def recipe_135() -> Dict[str, object]:
    return get_recipe(135)

def recipe_136() -> Dict[str, object]:
    return get_recipe(136)

def recipe_137() -> Dict[str, object]:
    return get_recipe(137)

def recipe_138() -> Dict[str, object]:
    return get_recipe(138)

def recipe_139() -> Dict[str, object]:
    return get_recipe(139)

def recipe_140() -> Dict[str, object]:
    return get_recipe(140)

def recipe_141() -> Dict[str, object]:
    return get_recipe(141)

def recipe_142() -> Dict[str, object]:
    return get_recipe(142)

def recipe_143() -> Dict[str, object]:
    return get_recipe(143)

def recipe_144() -> Dict[str, object]:
    return get_recipe(144)

def recipe_145() -> Dict[str, object]:
    return get_recipe(145)

def recipe_146() -> Dict[str, object]:
    return get_recipe(146)

def recipe_147() -> Dict[str, object]:
    return get_recipe(147)

def recipe_148() -> Dict[str, object]:
    return get_recipe(148)

def recipe_149() -> Dict[str, object]:
    return get_recipe(149)

def recipe_150() -> Dict[str, object]:
    return get_recipe(150)

def recipe_151() -> Dict[str, object]:
    return get_recipe(151)

def recipe_152() -> Dict[str, object]:
    return get_recipe(152)

def recipe_153() -> Dict[str, object]:
    return get_recipe(153)

def recipe_154() -> Dict[str, object]:
    return get_recipe(154)

def recipe_155() -> Dict[str, object]:
    return get_recipe(155)

def recipe_156() -> Dict[str, object]:
    return get_recipe(156)

def recipe_157() -> Dict[str, object]:
    return get_recipe(157)

def recipe_158() -> Dict[str, object]:
    return get_recipe(158)

def recipe_159() -> Dict[str, object]:
    return get_recipe(159)

def recipe_160() -> Dict[str, object]:
    return get_recipe(160)

def recipe_161() -> Dict[str, object]:
    return get_recipe(161)

def recipe_162() -> Dict[str, object]:
    return get_recipe(162)

def recipe_163() -> Dict[str, object]:
    return get_recipe(163)

def recipe_164() -> Dict[str, object]:
    return get_recipe(164)

def recipe_165() -> Dict[str, object]:
    return get_recipe(165)

def recipe_166() -> Dict[str, object]:
    return get_recipe(166)

def recipe_167() -> Dict[str, object]:
    return get_recipe(167)

def recipe_168() -> Dict[str, object]:
    return get_recipe(168)

def recipe_169() -> Dict[str, object]:
    return get_recipe(169)

def recipe_170() -> Dict[str, object]:
    return get_recipe(170)

def recipe_171() -> Dict[str, object]:
    return get_recipe(171)

def recipe_172() -> Dict[str, object]:
    return get_recipe(172)

def recipe_173() -> Dict[str, object]:
    return get_recipe(173)

def recipe_174() -> Dict[str, object]:
    return get_recipe(174)

def recipe_175() -> Dict[str, object]:
    return get_recipe(175)

def recipe_176() -> Dict[str, object]:
    return get_recipe(176)

def recipe_177() -> Dict[str, object]:
    return get_recipe(177)

def recipe_178() -> Dict[str, object]:
    return get_recipe(178)

def recipe_179() -> Dict[str, object]:
    return get_recipe(179)

def recipe_180() -> Dict[str, object]:
    return get_recipe(180)
