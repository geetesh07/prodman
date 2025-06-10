# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import nts

no_cache = 1


def get_context(context):
	homepage = nts.get_cached_doc("Homepage")

	homepage.title = homepage.title or homepage.company
	context.title = homepage.title
	context.homepage = homepage

	if homepage.hero_section_based_on == "Homepage Section" and homepage.hero_section:
		homepage.hero_section_doc = nts.get_cached_doc("Homepage Section", homepage.hero_section)

	if homepage.slideshow:
		doc = nts.get_cached_doc("Website Slideshow", homepage.slideshow)
		context.slideshow = homepage.slideshow
		context.slideshow_header = doc.header
		context.slides = doc.slideshow_items

	context.blogs = nts.get_all(
		"Blog Post",
		fields=["title", "blogger", "blog_intro", "route"],
		filters={"published": 1},
		order_by="modified desc",
		limit=3,
	)

	# filter out homepage section which is used as hero section
	homepage_hero_section = homepage.hero_section_based_on == "Homepage Section" and homepage.hero_section
	homepage_sections = nts.get_all(
		"Homepage Section",
		filters=[["name", "!=", homepage_hero_section]] if homepage_hero_section else None,
		order_by="section_order asc",
	)
	context.homepage_sections = [
		nts.get_cached_doc("Homepage Section", name) for name in homepage_sections
	]

	context.metatags = context.metatags or nts._dict({})
	context.metatags.image = homepage.hero_image or None
	context.metatags.description = homepage.description or None
