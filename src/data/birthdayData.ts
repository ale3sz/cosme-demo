export interface BirthdayPromo {
  id: string;
  name: string;
  pricePerPerson: number;
  description: string;
  included: string[];
  recommended?: boolean;
}

export const birthdayPromos: BirthdayPromo[] = [
  {
    id: '1',
    name: 'Promo 1 · Clásica',
    pricePerPerson: 17000,
    description: 'Papas clásicas + Pizzas Muzza, Napolitana y Especial libres por persona. Ideal para previas o reuniones descontracturadas.',
    included: [
      'Papas fritas clásicas libres',
      'Pizzas artesanales al corte (Muzza, Napo, Especial) libres',
      'Sector reservado en salón',
      'Pista de baile y DJ a partir de las 00:00 hs',
    ],
  },
  {
    id: '2',
    name: 'Promo 2 · Full Libre (La Más Elegida)',
    pricePerPerson: 21000,
    description: 'Papas clásicas + Variedad de Pizzas + Sándwiches de carne braseada libres + DJ en vivo, cotillón LED y brindis.',
    included: [
      'Papas clásicas libres con dips',
      'Pizzas libres (Muzza, Fugazzeta, Napo, Especial)',
      'Sándwiches de carne braseada libres al pan casero',
      'DJ set en vivo retro 90s/2000s & cotillón flúo LED',
      'Brindis de cortesía para el homenajeado/a',
    ],
    recommended: true,
  },
  {
    id: '3',
    name: 'Promo 3 · Premium Cosme',
    pricePerPerson: 26000,
    description: 'El festejazo total: Parrilla al paso + Burgers con cheddar fundido en mesa + Barra libre de birra tirada durante la cena.',
    included: [
      'Entradas de tapeo rústico y papas rústicas',
      'Hamburguesas smash con show de cascada de cheddar',
      'Cortes de parrilla al pan y sándwiches gourmet',
      'Canilla libre de cerveza artesanal seleccionada (2 horas)',
      'Espacio VIP exclusivo + cotillón temático',
    ],
  },
];

export const guestOptions = [8, 12, 18, 25, 30];
