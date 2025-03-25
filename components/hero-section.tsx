import Link from "next/link"
import { Button } from "@/components/ui/button"

export function HeroSection() {
  return (
    <div className="relative">
      <div className="absolute inset-0 bg-gradient-to-r from-black/60 to-black/30" />
      <div
        className="relative h-[70vh] flex items-center justify-start bg-cover bg-center"
        style={{ backgroundImage: "url('/placeholder.svg?height=1080&width=1920')" }}
      >
        <div className="container px-4 mx-auto">
          <div className="max-w-lg space-y-6 text-white">
            <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">New Season Collection</h1>
            <p className="text-lg md:text-xl">
              Discover our latest styles crafted with premium materials for exceptional comfort and timeless elegance.
            </p>
            <div className="flex flex-wrap gap-4">
              <Button asChild size="lg" className="bg-white text-black hover:bg-white/90">
                <Link href="/products">Shop Now</Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="text-white border-white hover:bg-white/10">
                <Link href="/products/new">New Arrivals</Link>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

