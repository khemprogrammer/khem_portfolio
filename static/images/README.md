# Project Images

This folder contains images for the portfolio website.

## Files Included:
- `favicon.svg` - Website favicon (already created)
- `profile_placeholder.svg` - Placeholder for profile image

## How to Add Your Own Images:

### 1. Profile Image
Upload your photo to: `media/profile/your-photo.jpg`
- Recommended size: 400x400px or larger
- Square format works best
- File format: JPG or PNG

### 2. Project Images
Upload project screenshots to: `media/projects/`
- Recommended size: 800x500px (16:10 aspect ratio)
- File format: JPG or PNG

### 3. Project Thumbnails
Upload to: `media/projects/thumbnails/`
- Recommended size: 400x250px
- Used in project cards

### 4. Gallery Images
Upload to: `media/projects/gallery/`
- Full resolution images
- Used in project detail pages

## Quick Reference:

| Type | Location | Recommended Size |
|------|----------|------------------|
| Profile | media/profile/ | 400x400px |
| Projects | media/projects/ | 800x500px |
| Thumbnails | media/projects/thumbnails/ | 400x250px |
| Gallery | media/projects/gallery/ | 1200x800px |

## Notes:
- The website will automatically use these images when uploaded via Django Admin
- Images are referenced in the database, not directly in this folder
- Go to Admin Panel > Portfolio/Projects to add images
- Keep file sizes under 500KB for better performance