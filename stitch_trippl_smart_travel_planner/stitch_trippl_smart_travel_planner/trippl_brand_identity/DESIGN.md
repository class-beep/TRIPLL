---
name: TRIPPL Brand Identity
colors:
  surface: '#f6faf9'
  surface-dim: '#d7dbda'
  surface-bright: '#f6faf9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f4f3'
  surface-container: '#ebefee'
  surface-container-high: '#e5e9e8'
  surface-container-highest: '#dfe3e2'
  on-surface: '#181c1c'
  on-surface-variant: '#3e4949'
  inverse-surface: '#2c3131'
  inverse-on-surface: '#edf2f1'
  outline: '#6e7979'
  outline-variant: '#bdc9c8'
  surface-tint: '#006a6a'
  primary: '#006565'
  on-primary: '#ffffff'
  primary-container: '#008080'
  on-primary-container: '#e3fffe'
  inverse-primary: '#76d6d5'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e4e2e1'
  on-secondary-container: '#656464'
  tertiary: '#8b4823'
  on-tertiary: '#ffffff'
  tertiary-container: '#a96039'
  on-tertiary-container: '#fff9f7'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#93f2f2'
  primary-fixed-dim: '#76d6d5'
  on-primary-fixed: '#002020'
  on-primary-fixed-variant: '#004f4f'
  secondary-fixed: '#e4e2e1'
  secondary-fixed-dim: '#c8c6c6'
  on-secondary-fixed: '#1b1c1c'
  on-secondary-fixed-variant: '#474747'
  tertiary-fixed: '#ffdbcb'
  tertiary-fixed-dim: '#ffb692'
  on-tertiary-fixed: '#341100'
  on-tertiary-fixed-variant: '#733512'
  background: '#f6faf9'
  on-background: '#181c1c'
  surface-variant: '#dfe3e2'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Work Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Work Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-sm:
    fontFamily: Work Sans
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1280px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style
The design system for this modern travel planning platform is rooted in a **Refined Minimalist** aesthetic. It prioritizes clarity and ease of navigation to reduce the cognitive load of trip planning. The brand personality is adventurous yet organized, evoking the feeling of a well-planned itinerary. 

The visual language uses generous whitespace to create a "breathable" interface, ensuring that high-quality travel photography remains the focal point. The emotional response should be one of confidence and excitement, achieved through crisp execution, deliberate alignment, and a sophisticated balance between utilitarian structure and editorial flair.

## Colors
The palette is anchored by a "Travel Teal" primary color, chosen for its association with depth and tranquility. A "Sunset Orange" is reserved for high-priority calls to action and success states.

- **Primary (Travel Teal):** Used for primary buttons, active navigation states, and interactive icons.
- **Secondary (Dark Charcoal):** The primary color for typography and high-contrast UI borders.
- **Background (Off-White):** A soft `#FAFAFA` base to reduce eye strain compared to pure white.
- **Muted Gray:** Used for dividers, disabled states, and placeholder text to maintain the minimal aesthetic.

## Typography
This design system utilizes a pairing of **Plus Jakarta Sans** for headings and **Work Sans** for body and interface text. 

Headings should always be bold to provide a strong structural anchor for the page. Body text is kept light or regular to ensure readability in content-heavy itinerary sections. For labels and small metadata (e.g., flight durations, prices), use uppercase Work Sans with slight letter spacing to differentiate from standard paragraph text.

## Layout & Spacing
The layout follows a **Fixed-Fluid Hybrid Grid**. On desktop, content is contained within a 1280px max-width container, centered on the screen. 

- **Grid Model:** A 12-column system with 24px gutters. 
- **Vertical Rhythm:** A strict 8px baseline grid is used for all internal component spacing (padding, margins between text and icons).
- **Responsive Behavior:** On tablet (under 1024px), margins shrink to 32px. On mobile (under 640px), the layout collapses to a single column with 20px side margins and 16px gutters.

## Elevation & Depth
Depth is created through **Ambient Shadows** and **Tonal Layers** rather than heavy borders.

1.  **Level 0 (Base):** The `#FAFAFA` background.
2.  **Level 1 (Cards):** Pure white background (`#FFFFFF`) with a very soft, diffused shadow: `0 4px 20px rgba(0,0,0,0.04)`.
3.  **Level 2 (Dropdowns/Modals):** Pure white background with a more defined shadow: `0 12px 40px rgba(0,0,0,0.08)`.
4.  **Dividers:** 1px solid lines using a light gray (`#EDEDED`) are used sparingly to separate vertical content sections without breaking the flow.

## Shapes
To reinforce the friendly and modern persona, a consistent **Rounded** geometry is applied across all components.

- **Standard Elements:** Buttons, input fields, and small cards use a 12px (`0.75rem`) radius.
- **Large Containers:** Hero sections and primary content cards use a 24px (`1.5rem`) radius.
- **Selection Indicators:** Small badges or tags use a pill-shape (full radius) for high contrast against rectangular layout elements.

## Components
- **Buttons:** Primary buttons use the Travel Teal background with white text and no border. Secondary buttons use a transparent background with a 1px Dark Charcoal border.
- **Cards:** Travel cards (for destinations or hotels) should feature a top-heavy image with a 12px corner radius. Content below the image should have ample padding (20px+) to maintain the minimal feel.
- **Input Fields:** Search inputs should be large with a 12px radius, a subtle 1px border, and a "Travel Teal" focus state.
- **Chips/Tags:** Used for categories (e.g., "Eco-friendly," "Luxury"). These use a light teal tint background with dark teal text.
- **Icons:** Use 2px stroke-width line icons. Icons should always be accompanied by labels in "label-sm" typography unless their function is universal (e.g., a search magnifying glass).
- **Lists:** Itinerary lists should use vertical lines to connect timeline dots, styled in the light divider color to remain unobtrusive.