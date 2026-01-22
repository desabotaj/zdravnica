# TechRepair Pro - UI/UX Design System

A modern, responsive UI design for a tech repair service featuring both a customer-facing landing page and an internal admin dashboard (CRM).

## 🎨 Design Features

### Design System
- **Color Palette**: Professional blues and greys with orange/green accents
- **Typography**: Clean, accessible Inter font family
- **Components**: Consistent buttons, cards, inputs, badges, and data tables
- **Spacing**: Systematic spacing scale for visual consistency
- **Animations**: Subtle scroll-reveal animations and hover effects

### Landing Page (`index.html`)
- ✅ Hero section with compelling headline and CTA
- ✅ Services section with 4 common repair types
- ✅ Trust indicators (warranty, certifications, repair time, ratings)
- ✅ Testimonials carousel
- ✅ Contact form with device selection
- ✅ Map embed placeholder
- ✅ Fully responsive, mobile-first design
- ✅ Smooth scroll animations

### Admin Dashboard (`admin.html`)
- ✅ Sidebar navigation with 6 main sections
- ✅ Dashboard overview with 4 stat cards and mini charts
- ✅ Repair Orders data table with status tags
- ✅ New Order modal with comprehensive form
- ✅ Customer profile view with repair history
- ✅ Responsive design with mobile menu
- ✅ Clean data visualization

## 📁 File Structure

```
avito/
├── index.html              # Landing page
├── admin.html              # Admin dashboard
├── styles/
│   ├── design-system.css  # Core design system
│   ├── landing.css        # Landing page styles
│   └── admin.css          # Admin dashboard styles
└── README.md              # This file
```

## 🚀 Getting Started

1. **Open the landing page**: Simply open `index.html` in your web browser
2. **Access admin dashboard**: Open `admin.html` or click "Admin Login" from the landing page
3. **No build process required**: This is static HTML/CSS - ready to use!

## 🎯 Key Features

### Landing Page
- **Hero Section**: Eye-catching gradient background with clear value proposition
- **Services Grid**: 4 service cards with icons (Screen, Battery, Water Damage, Software)
- **Trust Indicators**: 4 key metrics displayed prominently
- **Testimonials**: Customer review carousel (ready for multiple testimonials)
- **Contact Form**: Full form with validation and device type selection
- **Responsive**: Works perfectly on mobile, tablet, and desktop

### Admin Dashboard
- **Dashboard Overview**: 
  - Today's appointments
  - Pending repairs
  - Monthly revenue
  - Completed repairs this week
- **Repair Orders Table**: 
  - Status badges (In Progress, Ready, Completed)
  - Device type and customer info
  - Technician assignment
  - ETA tracking
  - Edit/Delete actions
- **New Order Modal**: 
  - Customer information
  - Device details
  - Issue description
  - Parts needed
  - Technician assignment
  - Estimated completion
- **Customer Profile**: 
  - Customer details
  - Repair statistics
  - Complete repair history

## 🎨 Design System Components

### Colors
- **Primary Blue**: `#2563eb` - Main brand color
- **Secondary Grey**: `#64748b` - Text and borders
- **Accent Orange**: `#f97316` - CTAs and highlights
- **Accent Green**: `#10b981` - Success states

### Typography
- **Headings**: Inter, bold, clear hierarchy
- **Body**: System font stack for optimal performance
- **Sizes**: Responsive scaling for mobile devices

### Components
- **Buttons**: Primary, Secondary, Accent variants with hover effects
- **Cards**: Elevated cards with subtle shadows
- **Inputs**: Clean form inputs with focus states
- **Badges**: Color-coded status indicators
- **Tables**: Clean, scannable data tables

## 📱 Responsive Breakpoints

- **Mobile**: < 768px - Single column layouts, mobile menu
- **Tablet**: 768px - 1024px - Adaptive grid layouts
- **Desktop**: > 1024px - Full multi-column layouts

## ✨ Animations

- **Scroll Reveal**: Elements fade in as user scrolls
- **Hover Effects**: Subtle lift and shadow on interactive elements
- **Smooth Transitions**: 250ms ease-in-out for all interactions

## 🔧 Customization

All design tokens are defined in CSS variables in `styles/design-system.css`. You can easily customize:
- Colors
- Spacing
- Typography
- Border radius
- Shadows
- Transitions

## 📝 Notes

- This is a high-fidelity static design - no backend integration
- Forms include client-side validation but don't submit to a server
- Testimonials carousel is set up but currently shows one testimonial
- Map embed is a placeholder - replace with actual Google Maps embed code
- All icons use emoji for simplicity - can be replaced with icon fonts or SVGs

## 🎯 Next Steps (Optional Enhancements)

1. Add actual Google Maps embed to contact section
2. Implement multi-testimonial carousel functionality
3. Add dark mode toggle
4. Connect forms to backend API
5. Add data persistence (localStorage or database)
6. Implement search and filtering for admin tables
7. Add export functionality for reports
8. Include more detailed charts/graphs

---

**Designed with ❤️ for modern tech repair services**
