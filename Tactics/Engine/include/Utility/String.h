#pragma once

#include <string>
#include <vector>
#include <set>
#include <sstream>
#include <string_view>
#include <chrono>
#include <span>

namespace Engine
{
    std::vector<std::string_view> Split(std::string_view str, char delimiter);
    std::set<std::string_view> SplitSet(std::string_view str, char delimiter);
	extern const std::string_view whitespace;
    std::string_view Strip(std::string_view, std::string_view trash = whitespace);
    std::string UpperCase(std::string_view str);
    std::string TitleCase(std::string_view str);
    std::string LowerCase(std::string_view str);
    std::string FormatDuration(double seconds);
    std::string FormatDuration(std::chrono::milliseconds);
    std::string Join(std::span<std::string_view> strs, std::string_view separator="");
    std::string Join(std::span<std::string> strs, std::string_view separator="");

    template<class T>
    std::string ToString(const T& object)
    {
        std::stringstream stream;
        stream << object;
        return stream.str();
    }

    struct Skip
    {
        explicit Skip(const std::string_view& skip) :
            characters(skip)
        {
        }
        std::string_view characters;
    };
    std::istream& operator>>(std::istream& s, Skip c);

    struct ReadChar
    {
    public:
        explicit ReadChar(char c) :
            character(c)
        {
        }
        char character;
    };
    std::istream& operator>>(std::istream& s, ReadChar c);

    struct ReadUntil
    {
        ReadUntil(char until, std::string& destination) :
            until(until),
            buffer(destination)
        {
        }

        char until;
        std::string& buffer;
    };
    std::istream& operator>>(std::istream& s, ReadUntil c);
}
