module.exports = {
  plugins: [
    require.resolve("@trivago/prettier-plugin-sort-imports"),
    require.resolve("prettier-plugin-tailwindcss"),
  ],
  // basic prettier settings
  printWidth: 80,
  trailingComma: "all",
  tabWidth: 2,
  semi: false,
  singleQuote: false,
  quoteProps: "consistent",
  arrowParens: "always",
  bracketSpacing: false,
  // prettier-plugin-sort-imports
  importOrder: [
    "^@/lib/(.*)$",
    "^@/utils/(.*)$",
    "^@/gql/?(.*)$",
    "^@/components/(.*)$",
    "^@/assets/(.*)$",
    "^[./]",
    "<THIRD_PARTY_MODULES>",
  ],
  importOrderSeparation: true,
  importOrderSortSpecifiers: true,
}
