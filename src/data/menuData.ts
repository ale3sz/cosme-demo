export interface MenuItem {
  id: string;
  title: string;
  badge: string;
  price?: string;
  description: string;
  image?: string;
  alt?: string;
  bullets: string[];
  isWide?: boolean;
}

export const nightMenu: MenuItem[] = [
  {
    id: 'cheddar',
    title: 'Cascada de Queso Cheddar',
    badge: 'Hit Nocturno · Show en Mesa',
    price: 'Show en Mesa',
    description: 'Dobles smash burgers selladas a la chapa y bañadas en vivo frente a vos con nuestra fuente de queso cheddar fundido bien caliente.',
    image: '/assets/cascada-cheddar.jpg',
    alt: 'Hamburguesa smash bañada en vivo por cascada de cheddar caliente',
    bullets: ['Doble medallón smash', 'Fuente cheddar hirviendo', 'Papas rústicas con dip'],
  },
  {
    id: 'parrilla',
    title: 'Carlito Rosarino de Vacío & Parrilla Libre',
    badge: 'Sello Rosario',
    price: '$29.500',
    description: 'Nuestro tributo a la ciudad: tostado rosarino relleno de vacío braseado 6 horas, más noches especiales de Parrilla Libre ilimitada.',
    image: '/assets/parrilla-cosme.jpg',
    alt: 'Cartel neón rojo COSME anunciando Parrilla Libre',
    bullets: ['Vacío braseado 6 hs', 'Parrilla Libre $29.500', 'Para compartir en barra'],
  },
  {
    id: 'sushi',
    title: 'Sushi Flambeado con Soplete',
    badge: 'Barra Live · Fuego Vivo',
    price: 'Fuego en Barra',
    description: 'Piezas frescas de salmón selladas al fuego directo con soplete en la barra frente a vos para lograr ese contraste ahumado inconfundible.',
    image: '/assets/sushi-flambeado.jpg',
    alt: 'Rolls de sushi flambeados con soplete sobre la barra',
    bullets: ['Salmón premium flambeado', 'Sopleteado a la vista', 'Marida con IPA o Gin Tonic'],
  },
  {
    id: 'milanesa',
    title: 'Milanesa Libre en Torre',
    badge: '4+ Personas c/ Bebida',
    price: '$15.900 / pers.',
    description: 'El plan indiscutible para mandarle al grupo de amigos: pisos interminables de milanesa napolitana con huevos a caballo y papas libres.',
    image: '/assets/noche-fiesta-caja.jpg',
    alt: 'Salón nocturno de fiesta en Cosme Alberdi para grupos',
    bullets: ['Napolitana + a caballo', 'Papas rústicas libres', '4+ personas con bebida incluida'],
    isWide: true,
  },
  {
    id: 'tablas',
    title: 'Tablas "La Previa" & "La Fulanito"',
    badge: 'Madera Rústica · Para Grupos',
    price: 'Para Compartir',
    description: 'Tablas macizas cargadas de fiambres, quesos seleccionados y bocados calientes pensadas para arrancar la previa entre pintas artesanales bien frías.',
    image: '/assets/tragos-noche.jpg',
    alt: 'Pintas de cerveza artesanal, cócteles y tabla de picada',
    bullets: ['Tabla La Previa abundante', 'Tabla La Fulanito caliente', '12 canillas de cerveza tirada'],
    isWide: true,
  },
];

export const dayMenu: MenuItem[] = [
  {
    id: 'torre-merienda',
    title: 'Torres de Merienda de 3 Pisos',
    badge: 'Clásico de Alberdi · Para Compartir',
    price: 'Bandeja Triple',
    description: 'Bandejas metálicas de tres niveles colmadas de medialunas de manteca, tostadas en pan de masa madre, dips y pastelería artesanal del día.',
    image: '/assets/torre-merienda.jpg',
    alt: 'Torre de merienda artesanal de 3 pisos',
    bullets: ['Pan casero de masa madre', 'Medialunas & budines del día', 'Dips salados y dulces'],
  },
  {
    id: 'cafe-especialidad',
    title: 'Café de Especialidad & Barismo',
    badge: 'Desde 08:00 hs',
    price: 'Origen Seleccionado',
    description: 'Granos de especialidad tostados artesanalmente servidos en cerámica rústica con latte art impecable o en versión iced para las tardes de Bv. Rondeau.',
    image: '/assets/salon-dia-tolix.jpg',
    alt: 'Salón diurno con sillas Tolix y café de especialidad',
    bullets: ['Flat White & Espresso Tonic', 'Iced Caramel Macchiato', 'Leche vegetal sin cargo extra'],
  },
  {
    id: 'brunch',
    title: 'Brunch Saludable & Tostones',
    badge: 'Fresco de Mañana',
    price: 'Brunch Fresco',
    description: 'Bowls de yogur griego con granola casera y frutos rojos, chipás recién horneados y tostones generosos de palta sobre hogaza de campo.',
    image: '/assets/salon-dia-tolix.jpg',
    alt: 'Brunch saludable con yogur y chipás',
    bullets: ['Bowl yogur griego & chía', 'Chipás caseros calientes', 'Tostón de palta & huevos revueltos'],
  },
  {
    id: 'ejecutivos',
    title: 'Menús Ejecutivos Semanales',
    badge: 'Lun a Vie · Mediodía',
    price: 'Almuerzos Caseros',
    description: 'Opciones reconfortantes que rotan semanalmente en el pizarrón del salón, pensadas para cortar el mediodía frente al río con rapidez y sabor casero.',
    image: '/assets/barra-edison.jpg',
    alt: 'Barra del local con lámparas Edison',
    bullets: ['Plato principal + bebida', 'Recetas de estación', 'Wi-Fi de alta velocidad & tomas'],
  },
];
