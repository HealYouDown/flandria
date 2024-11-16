import {graphql} from "@/gql"

import {ModelViewerElement} from "@google/model-viewer"
import * as React from "react"

graphql(`
  fragment ModelFragment on Available3DModel {
    asset_path
    animation_name
    character_class
    gender
  }
`)

type ModelViewerProps = {
  src: string
  className?: string

  playAnimation?: boolean
  rotate?: boolean
  rotationPerSecond?: string
}

export function ModelViewer({
  src,
  className,
  playAnimation = true,
  rotate = true,
  rotationPerSecond = "10deg",
}: ModelViewerProps) {
  const ref = React.useRef<ModelViewerElement>()

  const setPlayAnimation = (play: boolean) => {
    if (!ref.current) return

    if (play) ref.current.play()
    else ref.current.pause()
  }

  React.useEffect(() => {
    setPlayAnimation(playAnimation)
  }, [playAnimation])

  // no matter what the prop is set to, it will default to true,
  // so we just don't include defaults in here
  const viewerProps = {
    "rotation-per-second": rotationPerSecond,
    ...(playAnimation ? {autoplay: true} : {}),
    ...(rotate ? {"auto-rotate": true} : {}),
  }

  return (
    <model-viewer
      ref={ref}
      src={src}
      class={className}
      camera-controls
      touch-action="pan-y"
      interaction-prompt="none"
      {...viewerProps}
    />
  )
}
