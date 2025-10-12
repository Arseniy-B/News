export type Source = {
  id?: string;
  name?: string;
}

export type NewsItem = {
  source: Source;
  author?: string | null;
  title: string;
  description?: string | null;
  url?: string | null;
  urlToImage?: string | null;
  publishedAt: Date; 
  content?: string | null;
}

export const CountryCode = {
  US: "US", // США
  RU: "RU", // Россия
  CN: "CN", // Китай
  GB: "GB", // Великобритания
  DE: "DE", // Германия
  FR: "FR", // Франция
  JP: "JP", // Япония
  IN: "IN", // Индия
  BR: "BR", // Бразилия
  CA: "CA", // Канада
  AU: "AU", // Австралия
  IT: "IT", // Италия
  ES: "ES", // Испания
  KR: "KR", // Южная Корея
  MX: "MX", // Мексика
} as const;
export type CountryCode = (typeof CountryCode)[keyof typeof CountryCode];

export const Category = {
  BUSINESS: "business",
  ENTERTAINMENT: "entertainment",
  GENERAL: "general",
  HEALTH: "health",
  SCIENCE: "science",
  SPORTS: "sports",
  TECHNOLOGY: "technology",
} as const;
export type Category = (typeof Category)[keyof typeof Category];

export interface TopHeadlinesFilter {
  country?: CountryCode | null;
  category?: Category | null;
  q?: string | null;
  pageSize?: number; // default 20
  page?: number;     // default 1
}

export const Filter: TopHeadlinesFilter = {
  country: CountryCode.US, 
  // category: Category.BUSINESS,
  // q: "экономика",
  pageSize: 20,
  page: 1
};

const USER_FILTER_KEY = "filters"

export const filterService = {
  set(filters: TopHeadlinesFilter) {
    const jsonFilters = JSON.stringify(filters, null, 2);
    localStorage.setItem(USER_FILTER_KEY, jsonFilters);
  },

  get(): TopHeadlinesFilter | null {
    const jsonFilters = localStorage.getItem(USER_FILTER_KEY);
    if (jsonFilters){
      const filters: TopHeadlinesFilter = JSON.parse(jsonFilters);
      return filters;
    }
    return null;
  },
}; 
