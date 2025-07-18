"use client"

import { useState } from "react"
import Image from "next/image"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight, Expand } from "lucide-react"

interface GameGalleryProps {
  coverImage: string
  images: string[]
  title: string
}

export function GameGallery({ coverImage, images, title }: GameGalleryProps) {
  const [selectedImage, setSelectedImage] = useState(0)
  const [isFullscreen, setIsFullscreen] = useState(false)

  const allImages = [coverImage, ...images]

  const nextImage = () => {
    setSelectedImage((prev) => (prev + 1) % allImages.length)
  }

  const prevImage = () => {
    setSelectedImage((prev) => (prev - 1 + allImages.length) % allImages.length)
  }

  return (
    <>
      <Card className="card-steam overflow-hidden">
        <div className="relative">
          {/* Main Image */}
          <div className="relative aspect-video bg-slate-800">
            <Image
              src={allImages[selectedImage] || "/placeholder.svg"}
              alt={`${title} - Imagem ${selectedImage + 1}`}
              fill
              className="object-cover"
            />

            {/* Navigation Arrows */}
            <Button
              variant="ghost"
              size="sm"
              onClick={prevImage}
              className="absolute left-2 top-1/2 transform -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white"
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>

            <Button
              variant="ghost"
              size="sm"
              onClick={nextImage}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white"
            >
              <ChevronRight className="h-4 w-4" />
            </Button>

            {/* Fullscreen Button */}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsFullscreen(true)}
              className="absolute top-2 right-2 bg-black/50 hover:bg-black/70 text-white"
            >
              <Expand className="h-4 w-4" />
            </Button>

            {/* Image Counter */}
            <div className="absolute bottom-2 right-2 bg-black/50 text-white text-sm px-2 py-1 rounded">
              {selectedImage + 1} / {allImages.length}
            </div>
          </div>

          {/* Thumbnail Strip */}
          <div className="p-4 bg-slate-800/50">
            <div className="flex gap-2 overflow-x-auto">
              {allImages.map((image, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedImage(index)}
                  className={`relative flex-shrink-0 w-20 h-12 rounded overflow-hidden border-2 transition-colors ${
                    selectedImage === index ? "border-blue-400" : "border-slate-600 hover:border-slate-500"
                  }`}
                >
                  <Image
                    src={image || "/placeholder.svg"}
                    alt={`Thumbnail ${index + 1}`}
                    fill
                    className="object-cover"
                  />
                </button>
              ))}
            </div>
          </div>
        </div>
      </Card>

      {/* Fullscreen Modal */}
      {isFullscreen && (
        <div className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4">
          <div className="relative max-w-7xl max-h-full">
            <Image
              src={allImages[selectedImage] || "/placeholder.svg"}
              alt={`${title} - Imagem ${selectedImage + 1}`}
              width={1200}
              height={675}
              className="max-w-full max-h-full object-contain"
            />

            <Button
              variant="ghost"
              onClick={() => setIsFullscreen(false)}
              className="absolute top-4 right-4 bg-black/50 hover:bg-black/70 text-white"
            >
              ✕
            </Button>

            <Button
              variant="ghost"
              onClick={prevImage}
              className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white"
            >
              <ChevronLeft className="h-6 w-6" />
            </Button>

            <Button
              variant="ghost"
              onClick={nextImage}
              className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white"
            >
              <ChevronRight className="h-6 w-6" />
            </Button>
          </div>
        </div>
      )}
    </>
  )
}
