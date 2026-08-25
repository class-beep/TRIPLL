---
name: Earth & Ink
colors:
  surface: '#fff8f6'
  surface-dim: '#e8d6cf'
  surface-bright: '#fff8f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff1eb'
  surface-container: '#fdeae3'
  surface-container-high: '#f7e4dd'
  surface-container-highest: '#f1dfd7'
  on-surface: '#231a15'
  on-surface-variant: '#554339'
  inverse-surface: '#392e29'
  inverse-on-surface: '#ffede6'
  outline: '#887368'
  outline-variant: '#dbc1b5'
  surface-tint: '#994609'
  primary: '#964406'
  on-primary: '#ffffff'
  primary-container: '#b65c21'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb68e'
  secondary: '#815439'
  on-secondary: '#ffffff'
  secondary-container: '#fec2a1'
  on-secondary-container: '#794d34'
  tertiary: '#5c6000'
  on-tertiary: '#ffffff'
  tertiary-container: '#747a00'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbca'
  primary-fixed-dim: '#ffb68e'
  on-primary-fixed: '#331200'
  on-primary-fixed-variant: '#773300'
  secondary-fixed: '#ffdbc9'
  secondary-fixed-dim: '#f5ba99'
  on-secondary-fixed: '#321301'
  on-secondary-fixed-variant: '#663d24'
  tertiary-fixed: '#e3ea6c'
  tertiary-fixed-dim: '#c7ce53'
  on-tertiary-fixed: '#1b1d00'
  on-tertiary-fixed-variant: '#464a00'
  background: '#fff8f6'
  on-background: '#231a15'
  surface-variant: '#f1dfd7'
typography:
  headline-lg:
    fontFamily: Eb Garamond
    fontSize: 40px
    fontWeight: '600'
    lineHeight: 48px
  headline-md:
    fontFamily: Eb Garamond
    fontSize: 32px
    fontWeight: '500'
    lineHeight: 40px
  body-lg:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.5px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 24px
  margin: 32px
---

# Earth & Ink Design System

## Brand & Style
Earth & Ink evokes a sense of grounded professionalism and organic warmth. The brand personality is intellectual yet approachable, combining the timeless authority of editorial design with modern, user-centric functionality. The target audience values clarity, substance, and a sophisticated aesthetic that feels curated rather than manufactured.

The design style is **Corporate / Modern with an Editorial lean**. It prioritizes high-quality typography and a balanced, semantic color palette to create an environment that feels stable, trustworthy, and deeply legible. It avoids unnecessary flourishes, focusing instead on structural harmony and clear information hierarchy.

## Colors
The color palette is derived from natural, earthy tones to provide a warm and readable interface. The system uses a **light color mode** as its default state.

- **Primary (#b95e23):** A rich, burnt terracotta used for key actions and branding elements.
- **Secondary (#9d6c50):** A muted clay tone used for supporting interface elements and subtle accents.
- **Tertiary (#7e8405):** A mossy olive green providing a sophisticated contrast for supplemental information or alternative actions.
- **Neutral (#82746e):** A warm taupe-grey used for text, borders, and surfaces to maintain a cohesive, organic feel without the starkness of pure black or cool grey.

## Typography
The typography system creates a classic editorial contrast between serif headlines and sans-serif body text. 

- **Headline Font:** Eb Garamond
- **Body Font:** Manrope
- **Label Font:** Manrope

**Eb Garamond** is used for headlines to provide a sense of heritage and intellectual depth. **Manrope** is used for body and label text to ensure maximum legibility and a contemporary feel across digital interfaces. This pairing balances the "ink on paper" tradition with "pixel perfect" modern requirements.

## Layout & Spacing
The system utilizes a **fluid grid** model with a consistent 8px rhythmic scale. Layouts are designed to feel spacious and intentional.

- **Mobile:** 4-column grid with 16px margins and 16px gutters.
- **Tablet:** 8-column grid with 24px margins and 20px gutters.
- **Desktop:** 12-column grid with 32px margins and 24px gutters.

Spacing should favor generous vertical breathing room to reflect the editorial brand personality.

## Elevation & Depth
The design uses **tonal layers** and subtle shadows to convey depth. Instead of heavy shadows, the system relies on soft, low-opacity "ambient" shadows with a slight warm tint (#82746e) to maintain the organic aesthetic. Surfaces are differentiated by slight shifts in neutral tonal values and hair-line borders (1px) in a muted neutral shade.

## Shapes
The shape language is **Rounded**, providing a friendly and modern counterpoint to the traditional serif typography. 

Standard components utilize a 0.5rem (8px) corner radius. Larger containers or cards should use 1rem (16px), while internal elements like tags or small buttons may use a slightly softer 0.25rem (4px) or a full pill shape where appropriate. This softened geometry keeps the "Earth & Ink" brand feeling approachable.

## Components
- **Buttons:** Primary buttons use the terracotta (#b95e23) background with white text. Secondary buttons use a neutral-toned border with the secondary color for text.
- **Input Fields:** Use 1px borders in the neutral shade with a 0.5rem radius. Focused states utilize a 2px primary color border.
- **Cards:** Elevated with a very soft ambient shadow and a 1rem (16px) corner radius.
- **Chips/Labels:** Use the tertiary olive (#7e8405) in a low-saturation background state with dark text for categorizations.
- **Navigation:** Clean, centered serif links for top-level navigation, with sans-serif Manrope for utility or footer links.