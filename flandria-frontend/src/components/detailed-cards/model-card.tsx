import {titleCase} from "@/utils/utils"

import {ModelFragmentFragment} from "@/gql/graphql"

import {ModelViewer} from "@/components/model-viewer"
import {Button} from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {Tooltip, TooltipContent, TooltipTrigger} from "@/components/ui/tooltip"

import "@google/model-viewer"
import {
  CircleAlertIcon,
  ListVideoIcon,
  PauseIcon,
  PlayIcon,
  RefreshCwIcon,
  RefreshCwOffIcon,
} from "lucide-react"
import * as React from "react"

type Model = ModelFragmentFragment

interface ModelCardProps {
  models: ModelFragmentFragment[]
}

function getDisplayNameFromModel(model: Model) {
  return (
    model?.animation_name ??
    (model?.character_class && model?.gender
      ? `${titleCase(model.character_class)} (${titleCase(model.gender)})`
      : undefined) ??
    model.asset_path
  )
}

function PlayToggleButton({
  playAnimation,
  setPlayAnimation,
}: {
  playAnimation: boolean
  setPlayAnimation: (b: boolean) => void
}) {
  return (
    <Tooltip delayDuration={0}>
      <TooltipTrigger asChild>
        <Button
          onClick={() => setPlayAnimation(!playAnimation)}
          size="icon"
          variant="ghost"
        >
          {playAnimation ? (
            <PauseIcon className="icon-size" />
          ) : (
            <PlayIcon className="icon-size" />
          )}
        </Button>
      </TooltipTrigger>
      <TooltipContent>
        <p>Play animation</p>
      </TooltipContent>
    </Tooltip>
  )
}

function RotateToggleButton({
  rotate,
  setRotate,
}: {
  rotate: boolean
  setRotate: (b: boolean) => void
}) {
  return (
    <Tooltip delayDuration={0}>
      <TooltipTrigger asChild>
        <Button onClick={() => setRotate(!rotate)} size="icon" variant="ghost">
          {rotate ? (
            <RefreshCwOffIcon className="icon-size" />
          ) : (
            <RefreshCwIcon className="icon-size" />
          )}
        </Button>
      </TooltipTrigger>
      <TooltipContent>
        <p>Auto-rotate</p>
      </TooltipContent>
    </Tooltip>
  )
}

function SelectModelButton({
  selectedModel,
  setSelectedModel,
  models,
}: {
  selectedModel: Model
  setSelectedModel: (m: Model) => void
  models: Model[]
}) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button size="icon" variant="ghost">
          <ListVideoIcon className="icon-size" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        {models.map((model) => {
          const name = getDisplayNameFromModel(model)
          const isActive = model.asset_path === selectedModel.asset_path

          return (
            <DropdownMenuItem
              className={isActive ? "font-bold" : undefined}
              onClick={() => setSelectedModel(model)}
              key={model.asset_path}
            >
              {name}
            </DropdownMenuItem>
          )
        })}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

export function ModelCard({models}: ModelCardProps) {
  const [selectedModel, setSelectedModel] = React.useState<Model>(models[0])
  const [playAnimation, setPlayAnimation] = React.useState(true)
  const [rotate, setRotate] = React.useState(true)

  React.useEffect(() => setSelectedModel(models[0]), [models])

  if (models.length === 0 || !selectedModel) return null

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between py-1">
        <div className="flex flex-col items-start">
          <CardTitle>Model</CardTitle>
          {models.length > 1 && (
            <small className="text-[10px] text-muted-foreground">
              {getDisplayNameFromModel(selectedModel)}
            </small>
          )}
        </div>

        <div className="flex items-center">
          <PlayToggleButton
            playAnimation={playAnimation}
            setPlayAnimation={setPlayAnimation}
          />
          <RotateToggleButton rotate={rotate} setRotate={setRotate} />
          {models.length > 1 && (
            <SelectModelButton
              selectedModel={selectedModel}
              setSelectedModel={setSelectedModel}
              models={models}
            />
          )}
        </div>
      </CardHeader>
      <CardContent className="h-[400px] p-0">
        <ModelViewer
          src={selectedModel.asset_path}
          className="h-full w-full"
          playAnimation={playAnimation}
          rotate={rotate}
        />
      </CardContent>
      <CardFooter className="border-t p-2">
        <Tooltip delayDuration={100}>
          <TooltipTrigger className="flex w-full items-center justify-center space-x-2">
            <CircleAlertIcon className="icon-size text-muted-foreground" />
            <span className="text-sm text-muted-foreground">
              experimental feature, expect bugs
            </span>
          </TooltipTrigger>
          <TooltipContent className="max-w-[300px]">
            <p>
              The model viewer is an experimental feature. Many things (like for
              example particle effects) do not (yet) work correctly, so expect
              bugs. Models may look different ingame.
              <br />
              <br />
              Please do not report any bugs from the model viewer.
              <br />
              <br />
              If you're an expert on 3d models and or <kbd>.nif</kbd> files,
              feel free to get in touch, because I am none of the above x)
            </p>
          </TooltipContent>
        </Tooltip>
      </CardFooter>
    </Card>
  )
}
