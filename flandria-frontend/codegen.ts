import {CodegenConfig} from "@graphql-codegen/cli"

const config: CodegenConfig = {
  schema: "./schema.graphql",
  ignoreNoDocuments: true,
  generates: {
    "./src/gql/": {
      documents: ["./src/**/*.tsx", "./src/**/*.ts"],
      preset: "client",
      plugins: [],
      presetConfig: {
        fragmentMasking: false,
      },
    },
  },
}

export default config
